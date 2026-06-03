"""Fixture loading and source provenance validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema import ALLOWED_SOURCES, Fixture, NormalizedFact, REQUIRED_FIXTURES, SourceRecord


class FixtureError(ValueError):
    """Raised when a synthetic fixture violates the Mission 007 contract."""


def load_fixture(path: str | Path) -> Fixture:
    fixture_path = Path(path)
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    _validate_top_level(data, fixture_path)
    records = tuple(_source_record(item) for item in data["source_records"])
    _validate_sources(data["sources"], records, fixture_path)
    normalized = tuple(_normalize_record(record) for record in records)
    _validate_expected_refs(data.get("expected", {}), records)
    return Fixture(
        path=fixture_path,
        fixture_id=data["fixture_id"],
        synthetic_only=data["synthetic_only"],
        timezone=data["timezone"],
        scenario=data["scenario"],
        sources=tuple(data["sources"]),
        source_records=records,
        normalized_facts=normalized,
        expected=data["expected"],
    )


def load_fixtures(directory: str | Path = "fixtures/dtu") -> list[Fixture]:
    fixtures = [load_fixture(path) for path in sorted(Path(directory).glob("*.json"))]
    found = {fixture.fixture_id for fixture in fixtures}
    missing = REQUIRED_FIXTURES - found
    if missing:
        raise FixtureError(f"missing required fixtures: {sorted(missing)}")
    return fixtures


def _validate_top_level(data: dict[str, Any], path: Path) -> None:
    required = {
        "fixture_id",
        "synthetic_only",
        "timezone",
        "scenario",
        "sources",
        "source_records",
        "expected",
    }
    missing = required - data.keys()
    if missing:
        raise FixtureError(f"{path} missing required keys: {sorted(missing)}")
    if data["synthetic_only"] is not True:
        raise FixtureError(f"{path} must be synthetic_only")
    if not data["fixture_id"].startswith("dtu_"):
        raise FixtureError(f"{path} fixture_id must be a DTU id")
    if data["timezone"] != "Atlantic/Canary":
        raise FixtureError(f"{path} timezone must stay explicit")


def _source_record(data: dict[str, Any]) -> SourceRecord:
    required = {"id", "source", "source_record_id", "domain", "observed_at", "ingested_at", "payload"}
    missing = required - data.keys()
    if missing:
        raise FixtureError(f"source record missing keys: {sorted(missing)}")
    if data["source"] not in ALLOWED_SOURCES:
        raise FixtureError(f"source not allowed: {data['source']}")
    if not (data["source"].startswith("synthetic_") or data["source"] == "manual_note"):
        raise FixtureError(f"non-synthetic source not allowed: {data['source']}")
    if not isinstance(data["payload"], dict):
        raise FixtureError(f"payload must be object for {data['id']}")
    return SourceRecord(
        id=data["id"],
        source=data["source"],
        source_record_id=data["source_record_id"],
        domain=data["domain"],
        observed_at=data["observed_at"],
        ingested_at=data["ingested_at"],
        payload=data["payload"],
    )


def _validate_sources(sources: list[str], records: tuple[SourceRecord, ...], path: Path) -> None:
    if not sources:
        raise FixtureError(f"{path} must declare at least one source")
    undeclared = {record.source for record in records} - set(sources)
    if undeclared:
        raise FixtureError(f"{path} has undeclared record sources: {sorted(undeclared)}")
    unknown = set(sources) - ALLOWED_SOURCES
    if unknown:
        raise FixtureError(f"{path} declares unknown sources: {sorted(unknown)}")


def _normalize_record(record: SourceRecord) -> NormalizedFact:
    return NormalizedFact(
        id=f"fact_{record.id}",
        domain=record.domain,
        observed_at=record.observed_at,
        value={
            "source": record.source,
            "source_record_id": record.source_record_id,
            "payload": record.payload,
        },
        provenance_refs=(record.id,),
    )


def _validate_expected_refs(expected: dict[str, Any], records: tuple[SourceRecord, ...]) -> None:
    record_ids = {record.id for record in records}
    for workflow in expected.get("workflows", {}).values():
        for ref in workflow.get("required_evidence_refs", []):
            if ref.startswith("derived_"):
                continue
            if ref not in record_ids:
                raise FixtureError(f"expected evidence ref does not exist: {ref}")

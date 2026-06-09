from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.request import Request, urlopen


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Mission 019 private deployment smoke.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--expect-localhost", action="store_true")
    parser.add_argument("--expect-tailscale", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    if args.expect_localhost == args.expect_tailscale:
        failures.append("choose exactly one of --expect-localhost or --expect-tailscale")

    health = _get_json(f"{args.base_url.rstrip('/')}/api/health", failures)
    if health:
        if health.get("status") != "ok":
            failures.append("health.status must be ok")
        if health.get("synthetic_only") is not True:
            failures.append("health.synthetic_only must be true")
        if health.get("local_only") is not True:
            failures.append("health.local_only must be true")

    workbench_html = _get_text(f"{args.base_url.rstrip('/')}/workbench/", failures)
    if workbench_html:
        title = TitleParser()
        title.feed(workbench_html)
        if "Personal Performance OS" not in title.title:
            failures.append("workbench title mismatch")
        if 'data-testid="workbench-title"' not in workbench_html:
            failures.append("workbench title mount missing")
        if 'src="/workbench/app.js"' not in workbench_html:
            failures.append("workbench app script missing")

    result = {
        "base_url": args.base_url,
        "failures": failures,
        "mode": "tailscale" if args.expect_tailscale else "localhost",
        "status": "fail" if failures else "pass"
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


def _get_json(url: str, failures: list[str]) -> dict:
    text = _get_text(url, failures)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        failures.append(f"{url} did not return JSON: {exc}")
        return {}


def _get_text(url: str, failures: list[str]) -> str:
    try:
        request = Request(url, headers={"User-Agent": "Mission019Smoke/1.0"})
        with urlopen(request, timeout=5) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                failures.append(f"{url} returned HTTP {status}")
                return ""
            return response.read().decode("utf-8")
    except URLError as exc:
        failures.append(f"{url} request failed: {exc}")
    except TimeoutError:
        failures.append(f"{url} request timed out")
    return ""


if __name__ == "__main__":
    raise SystemExit(main())

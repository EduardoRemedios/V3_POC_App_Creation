from __future__ import annotations

import unittest
from pathlib import Path

from ppos_core.workbench import bootstrap_payload
from ppos_core.storage import connect, migrate


ROOT = Path(__file__).resolve().parents[1]


class Mission011WorkbenchTests(unittest.TestCase):
    def test_workbench_contains_source_adapter_lab_mounts(self) -> None:
        html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
        for marker in [
            'data-testid="nav-imports"',
            'data-testid="view-imports"',
            'data-testid="source-adapter-lab"',
            'data-testid="manual-export-selector"',
            'data-testid="preview-manual-import"',
            'data-testid="commit-manual-import"',
            'data-testid="manual-import-preview"',
            'data-testid="manual-import-mapping"',
            'data-testid="manual-import-conflicts"',
            'data-testid="manual-import-audit"',
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, html)

    def test_workbench_js_calls_manual_import_api(self) -> None:
        js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
        for marker in [
            "/api/source-adapters",
            "/api/manual-exports",
            "/api/manual-imports/preview",
            "/api/manual-imports/commit-synthetic",
            "renderManualImportSession",
            "previewSelectedManualImport",
            "commitSelectedManualImport",
            "manual_export",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_bootstrap_includes_import_lab_metadata(self) -> None:
        conn = connect(":memory:")
        migrate(conn)
        payload = bootstrap_payload(conn)
        self.assertIn("source_adapters", payload)
        self.assertIn("manual_exports", payload)
        self.assertGreaterEqual(len(payload["source_adapters"]), 5)
        self.assertEqual(9, len(payload["manual_exports"]))
        self.assertIn("source-adapter-lab", payload["workbench_extensions"])


if __name__ == "__main__":
    unittest.main()

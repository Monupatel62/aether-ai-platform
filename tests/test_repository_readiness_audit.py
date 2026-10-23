import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from repository_readiness_audit import CANONICAL_REPOSITORIES, audit, has_application_source


class RepositoryReadinessAuditTests(unittest.TestCase):
    def test_manifest_has_exactly_33_unique_repositories(self):
        self.assertEqual(33, len(CANONICAL_REPOSITORIES))
        self.assertEqual(33, len(set(CANONICAL_REPOSITORIES)))

    def test_missing_repository_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            records = audit(Path(temporary))
        self.assertEqual(33, len(records))
        self.assertTrue(all(record["status"] == "missing" for record in records))

    def test_docs_only_repository_is_distinguished_from_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / CANONICAL_REPOSITORIES[0]
            (repo / "docs").mkdir(parents=True)
            (repo / "docs" / "README.md").write_text("# Docs", encoding="utf-8")
            self.assertFalse(has_application_source(repo))
            (repo / "src").mkdir()
            (repo / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
            self.assertTrue(has_application_source(repo))
            records = audit(root)
        self.assertEqual("source-present", records[0]["status"])
        self.assertEqual("missing", records[1]["status"])

    def test_generated_and_vendor_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / "node_modules" / "package").mkdir(parents=True)
            (repo / "node_modules" / "package" / "index.js").write_text("", encoding="utf-8")
            (repo / "dist").mkdir()
            (repo / "dist" / "bundle.js").write_text("", encoding="utf-8")
            self.assertFalse(has_application_source(repo))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Dependency-free tests for Brand Soul initialization and validation."""

from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


validator = load_module("brand_soul_validator", SKILL_ROOT / "scripts" / "validate_brand_repository.py")


class StructuralTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        template = SKILL_ROOT / "assets" / "brand-repository-template"
        import shutil

        shutil.copytree(template, self.root)
        for path in self.root.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                text = text.replace("{{BRAND_NAME}}", "Test Brand")
                text = text.replace("{{BRAND_ID}}", "test-brand")
                text = text.replace("{{FOUNDER_NAME}}", "Test Founder")
                text = text.replace("{{GENERATED_DATE}}", "2026-09-01")
                path.write_text(text, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_draft_template_is_valid_with_pending_warning(self):
        errors, warnings = validator.validate(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("awaits founder approval" in item for item in warnings))

    def approve_identity(self):
        identity = self.root / "identity.md"
        digest = hashlib.sha256(identity.read_bytes()).hexdigest()
        manifest = self.root / "brand-context.yaml"
        text = manifest.read_text(encoding="utf-8")
        text = text.replace("repository_status: draft", "repository_status: approved")
        text = text.replace("approval: pending_founder", "approval: founder_approved")
        text = text.replace('approved_by: ""', 'approved_by: "Test Founder"')
        text = text.replace('approved_at: ""', 'approved_at: "2026-09-01T12:00:00-04:00"')
        text = text.replace('sha256: ""', f'sha256: "{digest}"')
        manifest.write_text(text, encoding="utf-8")

    def test_approved_hash_is_accepted(self):
        self.approve_identity()
        errors, _ = validator.validate(self.root)
        self.assertEqual(errors, [])

    def test_tampered_identity_is_rejected(self):
        self.approve_identity()
        with (self.root / "identity.md").open("a", encoding="utf-8") as handle:
            handle.write("\nTampered.\n")
        errors, _ = validator.validate(self.root)
        self.assertTrue(any("approval hash mismatch" in item for item in errors))

    def test_path_escape_is_rejected(self):
        manifest = self.root / "brand-context.yaml"
        text = manifest.read_text(encoding="utf-8").replace("truth: truth.yaml", "truth: ../truth.yaml")
        manifest.write_text(text, encoding="utf-8")
        errors, _ = validator.validate(self.root)
        self.assertTrue(any("escapes the repository" in item for item in errors))

    def test_verified_record_without_evidence_is_rejected(self):
        (self.root / "truth.yaml").write_text(
            "truth_records:\n"
            "  - id: truth-001\n"
            "    epistemic_status: verified\n"
            "    evidence_ids: []\n",
            encoding="utf-8",
        )
        errors, _ = validator.validate(self.root)
        self.assertTrue(any("verified truth record has no evidence" in item for item in errors))

    def test_approved_repository_rejects_open_high_issue(self):
        self.approve_identity()
        (self.root / "governance" / "issues.yaml").write_text(
            "issues:\n  - id: issue-001\n    severity: high\n    status: open\n",
            encoding="utf-8",
        )
        errors, _ = validator.validate(self.root)
        self.assertTrue(any("open high-severity issue" in item for item in errors))


if __name__ == "__main__":
    unittest.main()

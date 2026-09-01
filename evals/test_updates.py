#!/usr/bin/env python3
"""Tests for Brand Soul version parsing and cached update checks."""

from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import check_for_updates
import update_skill


class UpdateCheckTests(unittest.TestCase):
    def test_semver_normalization(self):
        self.assertEqual(check_for_updates.normalized_version("v1.2.3"), "1.2.3")
        self.assertEqual(check_for_updates.parse_version("2.0.0"), (2, 0, 0))
        with self.assertRaises(ValueError):
            check_for_updates.parse_version("latest")

    def test_fresh_cache_avoids_network(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "update-check.json"
            cache.write_text(
                json.dumps(
                    {
                        "checked_at_epoch": time.time(),
                        "latest_version": "1.1.0",
                        "tag_name": "v1.1.0",
                        "release_url": "https://example.test/release",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"BRAND_SOUL_CACHE_DIR": directory}), mock.patch.object(
                check_for_updates, "read_local_version", return_value="1.0.0"
            ), mock.patch.object(check_for_updates, "fetch_latest_release") as fetch:
                result = check_for_updates.check()
            self.assertEqual(result["status"], "update_available")
            self.assertTrue(result["cached"])
            fetch.assert_not_called()

    def test_network_failure_is_non_blocking(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(
            os.environ, {"BRAND_SOUL_CACHE_DIR": directory}
        ), mock.patch.object(check_for_updates, "read_local_version", return_value="1.0.0"), mock.patch.object(
            check_for_updates, "fetch_latest_release", side_effect=OSError("offline")
        ):
            result = check_for_updates.check(force=True)
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["current_version"], "1.0.0")

    def test_auto_update_refuses_new_major_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()

            def fake_git(*args, **_kwargs):
                if args == ("remote", "get-url", "origin"):
                    return mock.Mock(stdout="https://github.com/CacaoWebStudio/brand-soul.git\n", returncode=0)
                if args == ("status", "--porcelain"):
                    return mock.Mock(stdout="", returncode=0)
                raise AssertionError(f"unexpected git call: {args}")

            release = {
                "status": "update_available",
                "latest_version": "2.0.0",
                "tag_name": "v2.0.0",
                "release_url": "https://example.test/v2",
            }
            with mock.patch.object(update_skill, "SKILL_ROOT", root), mock.patch.object(
                update_skill, "git", side_effect=fake_git
            ), mock.patch.object(
                check_for_updates, "read_local_version", return_value="1.5.0"
            ), mock.patch.object(
                check_for_updates, "check", return_value=release
            ), mock.patch("sys.argv", ["update_skill.py", "--auto"]):
                result = update_skill.main()
            self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()

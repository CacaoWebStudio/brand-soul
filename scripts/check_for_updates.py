#!/usr/bin/env python3
"""Check GitHub Releases for a newer stable Brand Soul version."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


RELEASE_API = "https://api.github.com/repos/CacaoWebStudio/brand-soul/releases/latest"
CACHE_TTL_SECONDS = 24 * 60 * 60
SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?$")


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid semantic version: {value!r}")
    return tuple(int(part) for part in match.groups())


def normalized_version(value: str) -> str:
    return ".".join(str(part) for part in parse_version(value))


def read_local_version(root: Path = SKILL_ROOT) -> str:
    return normalized_version((root / "VERSION").read_text(encoding="utf-8"))


def cache_path() -> Path:
    override = os.environ.get("BRAND_SOUL_CACHE_DIR")
    if override:
        return Path(override).expanduser() / "update-check.json"
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "brand-soul" / "update-check.json"


def load_cache(path: Path, max_age: int = CACHE_TTL_SECONDS) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - float(payload["checked_at_epoch"]) <= max_age:
            return payload
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None
    return None


def write_cache(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        temporary.replace(path)
    except OSError:
        # Update checks must never block the Skill because a cache is unwritable.
        pass


def fetch_latest_release(timeout: float = 5.0) -> dict[str, str]:
    request = urllib.request.Request(
        RELEASE_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "brand-soul-update-checker",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    return {
        "latest_version": normalized_version(payload["tag_name"]),
        "tag_name": payload["tag_name"],
        "release_url": payload["html_url"],
    }


def check(force: bool = False, timeout: float = 5.0) -> dict[str, Any]:
    current = read_local_version()
    path = cache_path()
    release: dict[str, Any] | None = None
    cached = False

    if not force:
        release = load_cache(path)
        cached = release is not None

    if release is None:
        try:
            release = fetch_latest_release(timeout=timeout)
            release["checked_at_epoch"] = time.time()
            write_cache(path, release)
        except (OSError, ValueError, KeyError, urllib.error.URLError, json.JSONDecodeError) as error:
            return {
                "status": "unavailable",
                "current_version": current,
                "latest_version": None,
                "release_url": None,
                "cached": False,
                "error": str(error),
            }

    latest = normalized_version(str(release["latest_version"]))
    if parse_version(latest) > parse_version(current):
        status = "update_available"
    elif parse_version(latest) == parse_version(current):
        status = "current"
    else:
        status = "ahead"

    return {
        "status": status,
        "current_version": current,
        "latest_version": latest,
        "tag_name": release.get("tag_name", f"v{latest}"),
        "release_url": release.get("release_url"),
        "cached": cached,
        "error": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Ignore the 24-hour cache.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--quiet", action="store_true", help="Print only when an update exists.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Network timeout in seconds.")
    args = parser.parse_args()

    try:
        result = check(force=args.force, timeout=args.timeout)
    except (OSError, ValueError) as error:
        result = {"status": "invalid_installation", "error": str(error)}
        if args.json:
            print(json.dumps(result, sort_keys=True))
        elif not args.quiet:
            print(f"Brand Soul update check unavailable: {error}")
        return 2

    if args.json:
        print(json.dumps(result, sort_keys=True))
    elif result["status"] == "update_available":
        print(
            f"Brand Soul {result['latest_version']} is available; "
            f"this installation is {result['current_version']}. "
            "Run: python3 scripts/update_skill.py"
        )
    elif not args.quiet:
        if result["status"] == "unavailable":
            print("Brand Soul update check unavailable; continuing with the installed version.")
        else:
            print(f"Brand Soul {result['current_version']} is {result['status']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

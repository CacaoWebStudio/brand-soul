#!/usr/bin/env python3
"""Safely update a Git-installed Brand Soul Skill to a stable release."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import check_for_updates


SKILL_ROOT = Path(__file__).resolve().parent.parent
OFFICIAL_REMOTE_MARKERS = (
    "github.com/CacaoWebStudio/brand-soul.git",
    "github.com/CacaoWebStudio/brand-soul",
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(SKILL_ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def fail(message: str, code: int = 1) -> int:
    print(f"Brand Soul was not updated: {message}", file=sys.stderr)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yes", action="store_true", help="Update without an interactive confirmation.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Non-interactive update within the installed major version; never cross a major version.",
    )
    parser.add_argument("--version", help="Install one explicit stable version, such as 1.2.0.")
    args = parser.parse_args()

    if not (SKILL_ROOT / ".git").exists():
        return fail("this installation is not a Git clone. Reinstall it from the official repository.")

    try:
        remote = git("remote", "get-url", "origin").stdout.strip()
    except subprocess.CalledProcessError:
        return fail("the Git remote named origin is missing.")
    if not any(marker in remote for marker in OFFICIAL_REMOTE_MARKERS):
        return fail(f"origin does not point to the official repository: {remote}")

    dirty = git("status", "--porcelain").stdout.strip()
    if dirty:
        return fail("the installation has local changes. Commit or remove them before updating.")

    current = check_for_updates.read_local_version()
    if args.version:
        target = check_for_updates.normalized_version(args.version)
        tag = f"v{target}"
        release_url = None
    else:
        result = check_for_updates.check(force=True)
        if result["status"] == "unavailable":
            return fail("GitHub Releases could not be reached; try again later.")
        target = result["latest_version"]
        tag = result.get("tag_name") or f"v{target}"
        release_url = result.get("release_url")

    current_tuple = check_for_updates.parse_version(current)
    target_tuple = check_for_updates.parse_version(target)
    if target_tuple <= current_tuple:
        print(f"Brand Soul {current} is already current for the requested release.")
        return 0
    if args.auto and target_tuple[0] > current_tuple[0]:
        return fail(
            f"automatic updates cannot cross from {current} to major version {target}. "
            f"Review {release_url or tag} and run the updater without --auto.",
            code=3,
        )

    try:
        git("fetch", "origin", "--tags", "--prune")
        git("rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}")
    except subprocess.CalledProcessError:
        return fail(f"the release target {tag} was not found in the official repository.")

    ancestor = git("merge-base", "--is-ancestor", "HEAD", f"refs/tags/{tag}", check=False)
    if ancestor.returncode != 0:
        return fail(
            "the installed commit cannot be fast-forwarded to the release. "
            "Reinstall or resolve the Git history manually."
        )

    if not (args.yes or args.auto):
        print(f"Update Brand Soul from {current} to {target} ({tag})?")
        if release_url:
            print(f"Release notes: {release_url}")
        answer = input("Continue? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Update cancelled.")
            return 0

    try:
        git("merge", "--ff-only", f"refs/tags/{tag}")
    except subprocess.CalledProcessError as error:
        return fail(error.stderr.strip() or "Git could not fast-forward to the release.")

    installed = check_for_updates.read_local_version()
    if installed != target:
        return fail(f"release tag {tag} declares VERSION {installed}, expected {target}.")
    print(f"Brand Soul updated to {installed}. Start a new agent session to load it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

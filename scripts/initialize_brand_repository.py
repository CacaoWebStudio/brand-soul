#!/usr/bin/env python3
"""Initialize a Brand Soul V1 repository from the bundled template."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "brand-repository-template"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "brand"


def replace_tokens(root: Path, replacements: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token, value in replacements.items():
            content = content.replace(token, value)
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_parent", type=Path, help="Existing directory that will contain the new repository")
    parser.add_argument("--brand-name", required=True, help="Human-facing brand name")
    parser.add_argument("--founder", required=True, help="Founder who may approve protected Identity")
    parser.add_argument("--directory-name", help="Directory name; defaults to brand-soul-<brand-slug>")
    args = parser.parse_args()

    parent = args.output_parent.expanduser().resolve()
    if not parent.is_dir():
        parser.error(f"output parent is not an existing directory: {parent}")
    if not TEMPLATE_ROOT.is_dir():
        parser.error(f"template is missing: {TEMPLATE_ROOT}")

    directory_name = args.directory_name or f"brand-soul-{slugify(args.brand_name)}"
    if Path(directory_name).name != directory_name or directory_name in {".", ".."}:
        parser.error("directory name must be one safe path segment")
    destination = parent / directory_name
    if destination.exists():
        parser.error(f"destination already exists: {destination}")

    shutil.copytree(TEMPLATE_ROOT, destination)
    replace_tokens(
        destination,
        {
            "{{BRAND_NAME}}": args.brand_name,
            "{{BRAND_ID}}": slugify(args.brand_name),
            "{{FOUNDER_NAME}}": args.founder,
            "{{GENERATED_DATE}}": date.today().isoformat(),
        },
    )
    print(destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())

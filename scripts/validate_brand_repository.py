#!/usr/bin/env python3
"""Validate the structural safety of a Brand Soul V1 repository without dependencies."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "contract_version",
    "brand",
    "repository_status",
    "brand_state",
    "canonical_files",
    "governance_files",
    "protected_files",
    "consumer_rules",
}
REPOSITORY_STATUSES = {"draft", "usable_with_gaps", "approved"}
MATURITY = {"new", "emerging", "existing"}
EVIDENCE_COVERAGE = {"sparse", "partial", "substantial"}
IDENTITY_COHERENCE = {"undefined", "inconsistent", "coherent"}
APPROVALS = {"pending_founder", "founder_approved"}
REQUIRED_CANONICAL = {"truth", "identity", "voice", "strategy"}
REQUIRED_GOVERNANCE = {"claims", "issues", "evidence"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$")


class ParseError(ValueError):
    pass


def scalar(raw: str):
    value = raw.strip()
    if not value:
        return {}
    if value.startswith(('"', "'")):
        if len(value) < 2 or value[-1] != value[0]:
            raise ParseError(f"unterminated quoted scalar: {value}")
        return value[1:-1]
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_mapping(path: Path) -> dict:
    """Parse the mapping-only YAML subset used by brand-context.yaml."""
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for number, original in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        if "\t" in original[: len(original) - len(original.lstrip())]:
            raise ParseError(f"line {number}: tabs are not supported")
        indent = len(original) - len(original.lstrip(" "))
        if indent % 2:
            raise ParseError(f"line {number}: indentation must use multiples of two spaces")
        line = original.strip()
        if line.startswith("-"):
            raise ParseError(f"line {number}: lists are not supported in the manifest")
        if ":" not in line:
            raise ParseError(f"line {number}: expected key: value")
        key, raw = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
            raise ParseError(f"line {number}: unsupported key {key!r}")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ParseError(f"line {number}: invalid indentation")
        parent = stack[-1][1]
        if key in parent:
            raise ParseError(f"line {number}: duplicate key {key!r}")
        value = scalar(raw)
        parent[key] = value
        if isinstance(value, dict):
            stack.append((indent, value))
    return root


def nested(data: dict, *keys: str):
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_repo_path(root: Path, raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw:
        errors.append(f"{label} must be a non-empty relative path")
        return None
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label} escapes the repository: {raw}")
        return None
    return candidate


def collect_declared_ids(path: Path, record_key: str) -> set[str]:
    text = path.read_text(encoding="utf-8")
    if not re.search(rf"(?m)^{re.escape(record_key)}:\s*(?:\[\])?\s*$", text):
        return set()
    return set(re.findall(r"(?m)^\s*-\s+id:\s*[\"']?([a-z][a-z0-9-]+)", text))


def validate(root: Path) -> tuple[list[str], list[str]]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = root / "brand-context.yaml"
    if not manifest_path.is_file():
        return ["missing brand-context.yaml"], warnings
    try:
        data = parse_mapping(manifest_path)
    except (OSError, UnicodeError, ParseError) as exc:
        return [f"cannot parse brand-context.yaml: {exc}"], warnings

    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        errors.append(f"manifest missing top-level keys: {', '.join(sorted(missing))}")
    if data.get("contract_version") != 1:
        errors.append("contract_version must be 1")
    if data.get("repository_status") not in REPOSITORY_STATUSES:
        errors.append("repository_status is invalid")
    if nested(data, "brand_state", "maturity") not in MATURITY:
        errors.append("brand_state.maturity is invalid")
    if nested(data, "brand_state", "evidence_coverage") not in EVIDENCE_COVERAGE:
        errors.append("brand_state.evidence_coverage is invalid")
    if nested(data, "brand_state", "identity_coherence") not in IDENTITY_COHERENCE:
        errors.append("brand_state.identity_coherence is invalid")
    for key in ("id", "name"):
        if not nested(data, "brand", key):
            errors.append(f"brand.{key} is required")

    canonical = data.get("canonical_files", {})
    governance = data.get("governance_files", {})
    if not isinstance(canonical, dict) or not REQUIRED_CANONICAL.issubset(canonical):
        errors.append("canonical_files must name truth, identity, voice, and strategy")
        canonical = {}
    if not isinstance(governance, dict) or not REQUIRED_GOVERNANCE.issubset(governance):
        errors.append("governance_files must name claims, issues, and evidence")
        governance = {}
    for group_name, group in (("canonical_files", canonical), ("governance_files", governance)):
        for key, raw in group.items():
            path = safe_repo_path(root, raw, f"{group_name}.{key}", errors)
            if path is not None and not path.is_file():
                errors.append(f"missing declared file: {raw}")

    protected = data.get("protected_files", {})
    if not isinstance(protected, dict) or not protected:
        errors.append("protected_files must contain at least identity.md")
        protected = {}
    for raw_path, metadata in protected.items():
        path = safe_repo_path(root, raw_path, f"protected_files.{raw_path}", errors)
        if path is None or not path.is_file():
            errors.append(f"missing protected file: {raw_path}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"protected_files.{raw_path} must be a mapping")
            continue
        approval = metadata.get("approval")
        if approval not in APPROVALS:
            errors.append(f"protected_files.{raw_path}.approval is invalid")
            continue
        actual_hash = sha256(path)
        if approval == "founder_approved":
            if not metadata.get("approved_by") or not metadata.get("approved_at"):
                errors.append(f"approved protected file lacks approver or timestamp: {raw_path}")
            if metadata.get("sha256") != actual_hash:
                errors.append(f"approval hash mismatch for {raw_path}; actual sha256 is {actual_hash}")
        else:
            if any(metadata.get(key) for key in ("approved_by", "approved_at", "sha256")):
                warnings.append(f"pending protected file has approval metadata: {raw_path}")
            warnings.append(f"protected file awaits founder approval: {raw_path}; sha256 {actual_hash}")

    if data.get("repository_status") == "approved":
        for raw_path, metadata in protected.items():
            if not isinstance(metadata, dict) or metadata.get("approval") != "founder_approved":
                errors.append(f"approved repository contains unapproved protected file: {raw_path}")

    expected_rules = {
        "unresolved_claims": "prohibit_as_fact",
        "proposed_identity": "prohibit_as_canonical",
        "outdated_strategy": "exclude",
    }
    for key, value in expected_rules.items():
        if nested(data, "consumer_rules", key) != value:
            errors.append(f"consumer_rules.{key} must be {value}")

    evidence_path = safe_repo_path(root, governance.get("evidence"), "governance_files.evidence", errors) if governance else None
    truth_path = safe_repo_path(root, canonical.get("truth"), "canonical_files.truth", errors) if canonical else None
    if evidence_path and evidence_path.is_file() and truth_path and truth_path.is_file():
        evidence_ids = collect_declared_ids(evidence_path, "evidence_records")
        truth_text = truth_path.read_text(encoding="utf-8")
        active_truth_text = "\n".join(
            line for line in truth_text.splitlines() if not line.lstrip().startswith("#")
        )
        for evidence_id in set(re.findall(r"evidence-[0-9]+", active_truth_text)):
            if evidence_id not in evidence_ids:
                errors.append(f"truth.yaml references undeclared evidence ID: {evidence_id}")
        verified_blocks = re.split(r"(?m)^\s*-\s+id:\s*", active_truth_text)[1:]
        for block in verified_blocks:
            record_id = block.splitlines()[0].strip().strip("\"'")
            if "epistemic_status: verified" in block and re.search(r"evidence_ids:\s*\[\s*\]", block):
                errors.append(f"verified truth record has no evidence: {record_id}")
            if record_id and not ID_PATTERN.fullmatch(record_id):
                errors.append(f"invalid truth record ID: {record_id}")

    issues_path = safe_repo_path(root, governance.get("issues"), "governance_files.issues", errors) if governance else None
    if data.get("repository_status") == "approved" and issues_path and issues_path.is_file():
        issues_text = issues_path.read_text(encoding="utf-8")
        blocks = re.split(r"(?m)^\s*-\s+id:\s*", issues_text)[1:]
        for block in blocks:
            if "severity: high" in block and "status: open" in block:
                errors.append("approved repository has an open high-severity issue")
                break
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    root = args.repository.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    errors, warnings = validate(root)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"INVALID: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"VALID: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Brand Context Contract V1

## Contents

- Consumer procedure
- Required files
- Classification axes
- Record contracts
- Approval hashes
- Validation boundaries

## Consumer procedure

1. Open `brand-context.yaml` as the only entry point.
2. Require `contract_version: 1` and every path named under `canonical_files` and `governance_files`.
3. Verify protected-file hashes before relying on approved identity.
4. Read open high-severity issues before generating brand-facing work.
5. Load only the layers needed for the task, plus claims and relevant boundaries.
6. Exclude outdated Strategy, prohibit unresolved claims as fact, and prohibit proposed Identity as canonical.
7. When the requested execution needs a claim that is unresolved, expired, prohibited, or supported only more narrowly, verify it at point of use, apply its required qualification, omit it, or ask the user for the missing evidence. Never upgrade it silently.
8. Treat open attention issues as instructions for downstream caution, not as proof that the Brand Soul itself is unusable.
9. Report invalid or insufficient context; never replace it with assumptions.
10. Run the semantic integrity check before final output.

## Required files

The generated repository contains `README.md`, `brand-context.yaml`, `truth.yaml`, `identity.md`, `voice.md`, `strategy.md`, `governance/evidence.yaml`, `governance/claims.yaml`, `governance/issues.yaml`, `governance/decisions/`, `governance/schemas/contract-v1.schema.json`, and `governance/changelog.md`.

`repository_status` is `draft`, `usable_with_gaps`, or `approved`. A structurally valid repository may remain incomplete.

## Classification axes

Use all relevant axes; never overload one status:

- `knowledge_kind`: `fact`, `interpretation`, `identity_decision`, `strategy_decision`, `expression_example`
- `epistemic_status`: `verified`, `discovered`, `inferred`, `contradicted`, `unresolved`
- `decision_status`: `not_applicable`, `proposed`, `decided`, `rejected`, `superseded`
- `currency`: `current`, `outdated`, `unknown`
- `approval_status`: `not_required`, `pending_founder`, `founder_approved`
- `confidence`: `high`, `medium`, `low`

`discovered` means present in a source, not proven. `verified` requires adequate evidence, currentness, and no unresolved material contradiction. Founder memory alone remains labeled as memory.

## Record contracts

Evidence records require stable `id`, `source_type`, `title`, `locator`, `observed_at`, `authority_rank`, `relevance`, `sensitive`, and optional fingerprint. Do not copy sensitive source material into Git by default.

Truth records require `id`, atomic `statement`, `subject`, `predicate`, `value`, classification axes, `evidence_ids`, `contradicts`, `last_reviewed`, and `notes`.

Claims require `id`, `claim`, `category`, `permission`, approved wording, required qualifiers, prohibited extensions, evidence IDs, and review date. Permissions are `approved`, `qualified_only`, `prohibited`, `unresolved`, or `expired`.

Issues require `id`, `type`, `severity`, `status`, `layer`, `summary`, related record IDs, next action, and timestamps. Types include proposal, contradiction, gap, question, and risk. Issue material is never canonical.

Decision files use YAML frontmatter with `id`, `date`, `status`, `layer`, `approved_by`, `supersedes`, and `affected_files`, followed by context, decision, rationale, alternatives, consequences, and reconsideration conditions.

## Approval hashes

Compute SHA-256 over the exact bytes of each protected file. Store lowercase hexadecimal output in `protected_files.<path>.sha256`. Editing even whitespace invalidates approval.

Approval requires `founder_approved`, the founder's name, an ISO-8601 timestamp, and the matching hash. A pending approval uses empty approval metadata and hash. Do not normalize Markdown before hashing.

## Validation boundaries

The bundled validator checks structure, manifest enums and paths, protected hashes, obvious cross-references, and unsafe status combinations. It cannot judge whether evidence is truthful, Identity is distinctive, or prose follows boundaries. Those require the reasoning-based audit in `references/evaluation.md`.

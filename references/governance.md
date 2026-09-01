# Brand Soul Governance

## Contents

- Layer permissions
- Founder approval
- Facts and claims
- Contradictions
- Updates and decisions
- Repository status

## Layer permissions

- **Truth:** evidence-required; revise when facts or evidence change.
- **Identity:** founder-approved and protected; challenge through issues, never silent edits.
- **Strategy:** explicit, challengeable, and revisable; do not promote it to Identity.
- **Expression:** temporary and optimizable within higher-layer constraints.

Evidence supports all layers but is not itself a content layer.

Mark records as protected, challengeable, temporary, or non-canonical. Protection does not make a record immune to contrary evidence; it controls the change procedure.

## Founder approval

Only the founder approves V1 protected Identity, principles, boundaries, material tensions, founder story, disputed historical interpretation, official Strategy decisions, contradictions involving founder intention, and reversals of protected decisions.

Objective facts may become verified without founder approval when evidence is adequate. Founder confirmation of undocumented history remains memory or acknowledged interpretation, not independent verification.

Approval must identify the exact material, founder, timestamp, and file hash. Any protected-file edit invalidates approval. Never update an approval hash merely to silence validation; obtain renewed explicit review first.

## Facts and claims

Make factual records atomic and evidence-linked. A record cannot be `verified` with no evidence, `inferred` and approved as fact, `outdated` and current, or materially contradicted without an open issue.

Claims govern repeatability rather than legal compliance. Use `qualified_only` when evidence supports a narrower statement. Treat health, environmental, cultural, performance, community, certification, and quantified claims as higher risk. Do not strengthen approved wording by paraphrase.

## Contradictions

State propositions neutrally, distinguish fact from intention and perception, compare source authority and dates, seek clarification, and retain contrary evidence. Resolve as corrected, intentionally plural, superseded, or unresolved. Every unresolved material contradiction receives an issue.

## Updates and decisions

1. Register new evidence.
2. Classify layer and change type: corrective, evolutionary, or expressive.
3. Identify contradictions, affected claims, decisions, and consumers.
4. Place proposed protected changes in the issue register.
5. Obtain approval when required.
6. Edit canonical files and preserve superseded rationale.
7. Add a decision record only when a future agent could otherwise misunderstand why the change exists.
8. Refresh valid approvals only after review, then validate.

Ordinary changes use Git history and decision records. Increment `contract_version` only for breaking changes to the consumer contract.

## Repository status

- `draft`: protected material is unapproved or critical discovery is incomplete.
- `usable_with_gaps`: sufficient for bounded use, with limitations and high-severity issues disclosed.
- `approved`: all protected hashes are valid, no hidden critical gaps remain, and completion gates pass.

Do not equate structural validity with approval or completeness.

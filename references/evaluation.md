# Brand Soul Evaluation

## Contents

- Brand Integrity Check
- Behavioral cases
- Cross-session evaluation
- Completion rubric

## Brand Integrity Check

For each dimension return `pass`, `fail`, or `cannot-determine`, cite record IDs or headings, explain the finding, and recommend remediation:

1. Fact integrity: no unsupported factual additions.
2. Identity integrity: no contradiction of approved principles or tensions.
3. Story integrity: no embellished history or collapsed memory/interpretation.
4. Claim integrity: wording obeys claim permission and qualifiers.
5. Boundary integrity: no protected refusal is crossed.
6. Cultural integrity: no invented authority, meaning, relationship, or context.
7. Voice integrity: behavior matches the voice model without mere keyword mimicry.
8. Positioning integrity: no silent repositioning or outdated Strategy.
9. Decision integrity: no conflict with an active material decision.
10. Distinctiveness: central meaning cannot transfer unchanged to a plausible competitor.

Run the deterministic validator first. Semantic review cannot rescue an invalid contract or stale approval.

## Behavioral cases

Use `evals/cases/*.yaml` as test specifications. Required cases cover generic identity, invented history, founder bias, strategy/truth separation, contradiction detection, excessive and insufficient interviewing, identity drift, generic voice, fact escalation, cultural invention, valid evolution, tampered approval, unsupported claims, and incomplete-but-usable repositories.

Evaluate traceability and behavior, not impressive prose. A case defines required behaviors, prohibited behaviors, and observable assertions.

## Cross-session evaluation

Use isolated contexts and expose only the approved repository after the build session:

1. Build from raw evidence and founder decisions.
2. Write a homepage.
3. Write an advertisement.
4. Write an email.
5. Audit all outputs.

Targets: zero unsupported facts, protected-boundary violations, Identity contradictions, or unapproved claims; at least 80% retention of required distinctive elements; at least 80% voice-rubric agreement; at least 90% seeded-violation recall; at most 10% false positives; no generic substitution failure in central messaging.

Include adversarial prompts that reward conversion-oriented drift. Do not leak expected answers, diagnoses, or intended fixes to forward-test agents.

## Completion rubric

A repository is complete only when material facts are traceable, contradictions remain visible, approval hashes are valid, Strategy is separable from protected layers, central Identity scores at least 6/8 on distinctiveness, and a fresh agent can consume it without the original conversation. Template population alone is never completion.

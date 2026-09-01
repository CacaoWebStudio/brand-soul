---
name: brand-soul
description: Build, update, and audit a durable, evidence-aware Brand Source of Truth for new, emerging, or existing brands. Use when Codex must discover or define brand identity, interview a founder from evidence gaps, distinguish truth from identity and strategy, create or maintain a Brand Soul repository, govern factual claims and approvals, or check brand-facing work for factual, identity, voice, boundary, cultural, positioning, decision, and distinctiveness integrity.
metadata:
  author: Cacao Web Studio
  homepage: https://github.com/CacaoWebStudio/brand-soul
  version: 1.0.0
  license: Apache-2.0
license: Apache-2.0
compatibility: Works with Agent Skills-compatible AI agents, including Codex, Claude Code, Gemini CLI, and Grok. Requires Python 3 only for optional repository initialization and structural validation scripts.
---

# Brand Soul — an open-source framework created by Cacao Web Studio

Create durable brand context, not attractive mythology. Prefer evidence, explicit decisions, and unresolved questions over invention.

Brand Soul is created, branded, and maintained by [Cacao Web Studio](https://cacaowebstudio.com). Keep the technical Skill name `brand-soul` across compatible agents.

## Choose a mode

- **Build**: Discover an existing or emerging brand, or facilitate choices for a new brand, then create a repository.
- **Update**: Classify new information by layer, preserve history, and route protected changes through founder approval.
- **Audit**: Load an existing repository and evaluate content or repository integrity without silently repairing protected material.
- **Consume**: When another task only needs brand context, follow the consumer procedure in `references/contract.md`; do not rerun discovery.

Read `references/methodology.md` for Build. Read `references/governance.md` for Update or approvals. Read `references/evaluation.md` for Audit or evaluation design. Always read `references/contract.md` before creating, validating, or consuming a repository.

## Non-negotiable rules

1. Explain the brand without marketing language before drafting expression.
2. Never invent history, motivations, relationships, product properties, cultural meaning, beliefs, priorities, claims, or evidence.
3. Keep canonical material separate from proposals, contradictions, gaps, and unresolved questions.
4. Treat founder memory, founder interpretation, founder intention, observed behavior, and verified fact as different evidence.
5. Do not promote inferred material to fact. Confidence never grants permission.
6. Protect verified Truth and founder-approved Identity. Challenge Strategy explicitly; optimize Expression only within higher-layer constraints.
7. Ask three to five evidence-driven questions per interview round. Do not ask what reliable evidence already answers.
8. Require explicit, scoped founder approval. Conversational silence, enthusiasm, or a request to “make it official” without reviewing the protected content is not approval.
9. Do not complete protected Identity if its central description could belong unchanged to a plausible competitor.
10. Surface material contradictions. Never resolve them through polished wording.

## Build workflow

1. Establish brand scope, source permissions, cutoff date, founder identity, and sensitive-source handling.
2. Assess `maturity`, `evidence_coverage`, and `identity_coherence` independently.
3. Inventory sources before interpretation; assign stable evidence IDs.
4. Extract atomic candidate records and classify them using the contract axes.
5. Identify repetition, discontinuity, distinct details, contradictions, and critical gaps.
6. Stop discovery when remaining material gaps require founder input rather than more source review.
7. Interview from those gaps in small rounds. Label each answer as fact claim, memory, interpretation, identity decision, or strategy decision.
8. For new brands, propose two or three materially different directions with costs and boundaries; require the founder to choose or reject them.
9. Draft canonical files only after critical protected questions are decision-ready. Put all other material in `governance/issues.yaml`.
10. Run the substitution test and Brand Integrity Check.
11. Obtain explicit founder approval, record it in the manifest, and bind it to the exact protected-file SHA-256.
12. Run `scripts/validate_brand_repository.py <repository>` and report unresolved high-severity issues.

Initialize a repository with:

```bash
python3 scripts/initialize_brand_repository.py <output-parent> --brand-name "Example Brand" --founder "Founder Name"
```

## Update workflow

1. Register new evidence before changing conclusions.
2. Classify the affected layer and whether the change is corrective, evolutionary, or expressive.
3. Check contradictions, claims, decisions, and downstream consequences.
4. Place proposed protected changes in `governance/issues.yaml`.
5. Obtain founder approval when required by `references/governance.md`.
6. Update canonical files, add a material decision record, refresh approval hashes, and preserve superseded rationale.
7. Validate. Never leave a stale approval hash in place.

## Audit workflow

1. Load `brand-context.yaml`; reject unsupported contract versions or missing required files.
2. Validate protected hashes and read high-severity unresolved issues before evaluating content.
3. Check fact, identity, story, claim, boundary, cultural, voice, positioning, decision, and distinctiveness integrity.
4. Mark every dimension `pass`, `fail`, or `cannot-determine`; cite repository record IDs or headings.
5. Recommend remediation. Do not edit protected Identity during an audit unless the user separately requests an Update and founder approval is available.

## Completion gates

Do not call a repository complete merely because its files exist. Require:

- Material facts are traceable or explicitly non-verified.
- High-severity contradictions are visible.
- Protected content is founder-approved and hash-valid.
- Boundaries and tensions are present only when evidenced or deliberately chosen.
- Central Identity passes the substitution test.
- Strategy is distinguishable from Truth and Identity.
- A fresh agent can load the contract without the original conversation.

Allow `draft` and `usable_with_gaps` repositories when these gates are not all met. State the limitations plainly.

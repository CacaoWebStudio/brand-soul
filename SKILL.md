---
name: brand-soul
description: Build, update, and audit a durable, evidence-aware Brand Source of Truth for new, emerging, or existing brands. Use when Codex must discover or define brand identity, interview a founder from evidence gaps, distinguish truth from identity and strategy, create or maintain a Brand Soul repository, govern factual claims and approvals, or check brand-facing work for factual, identity, voice, boundary, cultural, positioning, decision, and distinctiveness integrity.
metadata:
  author: Cacao Web Studio
  homepage: https://github.com/CacaoWebStudio/brand-soul
  version: 1.1.0
  license: Apache-2.0
license: Apache-2.0
compatibility: Works with Agent Skills-compatible AI agents, including Codex, Claude Code, Gemini CLI, and Grok. Requires Python 3 for optional initialization, validation, and update utilities; network access is optional and used only for release checks and user-authorized updates.
---

# Brand Soul — an open-source framework created by Cacao Web Studio

Create durable brand context, not attractive mythology. Prefer evidence, explicit decisions, and unresolved questions over invention.

Brand Soul is created, branded, and maintained by [Cacao Web Studio](https://cacaowebstudio.com). Keep the technical Skill name `brand-soul` across compatible agents.

## Update awareness

On the first Brand Soul turn of a session, when the bundled script, Python 3, and network execution are available, run this from the Brand Soul Skill directory (or use the script's absolute path):

```bash
python3 scripts/check_for_updates.py --json
```

The checker caches successful release results for 24 hours. If its status is `update_available`, tell the user once which installed and stable versions differ, include the release URL when returned, and offer `python3 scripts/update_skill.py`. Continue the requested Brand Soul work unless the user chooses to update. Treat `current`, `ahead`, `unavailable`, missing runtime, and network errors as silent and non-blocking.

Never modify the Skill installation merely because an update exists. Run `update_skill.py` only after the user explicitly requests an update. The `--auto` option is solely for a separately configured opt-in automation and must never cross a major version.

## Choose a mode

At the beginning of a user-facing Brand Soul session, present the available modes with the host's interactive elicitation or choice tool when one exists. Make the choices tappable; do not simulate buttons with an ordinary Markdown list. If the host has no interactive choice capability, present a short numbered fallback.

- **Build for an existing brand**: Research a brand that already has public or private evidence, then create its Brand Soul repository.
- **Build for a new brand idea**: Facilitate deliberate identity choices when the brand itself does not yet exist.
- **Update an existing Brand Soul**: Classify new information by layer, preserve history, and route protected changes through founder approval.
- **Audit or consume an existing Brand Soul**: Evaluate it or load approved context without rerunning discovery.

A missing Brand Soul repository, an empty workspace, or absent local evidence says nothing about brand maturity. Never classify a brand as new from repository state. Ask the user to choose between an existing brand and a new brand idea before selecting the Build path.

Read `references/methodology.md` for Build. Read `references/governance.md` for Update or approvals. Read `references/evaluation.md` for Audit or evaluation design. Always read `references/contract.md` before creating, validating, or consuming a repository.

## Non-negotiable rules

1. Explain the brand without marketing language before drafting expression.
2. Never invent history, motivations, relationships, product properties, cultural meaning, beliefs, priorities, claims, or evidence.
3. Keep canonical material separate from proposals, contradictions, gaps, and unresolved questions.
4. Treat founder memory, founder interpretation, founder intention, observed behavior, and verified fact as different evidence.
5. Do not promote inferred material to fact. Confidence never grants permission.
6. Protect verified Truth and founder-approved Identity. Challenge Strategy explicitly; optimize Expression only within higher-layer constraints.
7. Ask exactly one user-facing question per turn during onboarding and founder discovery. Wait for the answer before asking the next question, preserve all answers, and analyze them together during synthesis. Do not ask what reliable evidence already answers.
8. Require explicit, scoped founder approval. Conversational silence, enthusiasm, or a request to “make it official” without reviewing the protected content is not approval.
9. Do not complete protected Identity if its central description could belong unchanged to a plausible competitor.
10. Surface material contradictions. Never resolve them through polished wording.

## Build workflow

1. Use interactive mode selection to determine whether the user is building for an existing brand or a new brand idea. Do not infer this from the workspace.
2. For an existing brand, ask for the primary website as the first discovery question.
3. In later turns, ask separately for official social profiles; marketplace, retailer, directory, press, review, or app-store pages; and relevant private files. Do not combine these into a questionnaire.
4. Ask which markets, product lines, or business units the repository should cover only when the supplied sources do not make scope clear.
5. Establish source permissions and sensitive-source handling when access or storage requires them. Use the current date as the default evidence cutoff unless another cutoff materially matters.
6. Inspect accessible sources before interviewing the founder. Inventory them, assign stable evidence IDs, and extract factual claims, recurring language, offers, audiences, visual signals, chronology, contradictions, and gaps.
7. Assess `maturity`, `evidence_coverage`, and `identity_coherence` independently. Repository state is not evidence for any of these fields.
8. Return a concise evidence brief, then interview only from consequential gaps and contradictions. Ask exactly one concrete question per turn and state the observed evidence or gap that makes the answer necessary. Avoid abstract audit labels in user-facing wording.
9. Preserve each answer as a fact claim, memory, interpretation, Identity decision, or Strategy decision, but do not require the user to understand those internal classifications.
10. For new brands, gather business reality one concrete question at a time, then propose two or three materially different directions with costs and boundaries; require the founder to choose or reject them.
11. Draft canonical files only after critical protected questions are decision-ready. Put all other material in `governance/issues.yaml`.
12. Run the substitution test and Brand Integrity Check.
13. Obtain explicit founder approval, record it in the manifest, and bind it to the exact protected-file SHA-256.
14. Run `scripts/validate_brand_repository.py <repository>` and report unresolved high-severity issues.

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

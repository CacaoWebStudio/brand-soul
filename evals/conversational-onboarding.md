# Conversational onboarding behavioral evaluation

Use these cases in fresh sessions. Judge observable decisions, not exact wording.

## Case 1: existing brand, empty workspace

Prompt:

> Use $brand-soul to build a Brand Soul repository for Sacred Bean.

Required behavior:

- Present Build-existing, Build-new, Update, and Audit/Consume as tappable choices when the host supports interactive elicitation.
- Do not infer that Sacred Bean is new because the workspace or repository is empty.
- After the user chooses an existing brand, ask only for the primary website.
- Ask no second question until the user answers.
- Discover social profiles and other public sources from the website and public search.
- Present discovered sources for confirmation instead of asking the founder to list them.
- Inspect confirmed sources before asking the founder to restate brand facts.

Failure conditions:

- Declares the brand new or evidence-sparse from workspace state.
- Displays an ordinary Markdown list when an interactive choice tool is available.
- Asks two or more user-facing questions in one turn.
- Begins with abstract headings such as founder authority, brand scope, evidence cutoff, or source inventory.
- Asks the founder for information already available in supplied sources.
- Requests social, marketplace, press, or directory URLs before trying to discover them.
- Lets a clarification create an unlimited new chain of questions.
- Turns Build into an exhaustive documentation or claim audit.

## Case 2: new brand idea

Prompt:

> Use $brand-soul to help me build a brand that does not exist yet.

Required behavior:

- Recognize the explicit new-brand state without asking for a website.
- Gather business reality, constraints, offer, and intended market one concrete question per turn.
- Preserve answers for joint synthesis.
- Offer materially different directions only after enough concrete information exists.

## Case 3: existing brand with contradictory evidence

Prompt:

> Build a Brand Soul for my existing company. Its website is https://example.com and its Instagram is https://instagram.com/example.

Required behavior:

- Inspect both supplied sources before the founder interview when access is available.
- Summarize material evidence briefly.
- Ask one concrete question about the highest-impact contradiction or gap.
- Keep observed evidence separate from founder interpretation and decision.

## Case 4: host without interactive controls

Prompt:

> Use $brand-soul.

Required behavior:

- Present a short numbered mode choice.
- Ask the user to select one mode.
- Do not continue into discovery in the same turn.

## Case 5: website already links public sources

Prompt:

> Build a Brand Soul for my existing company. The website is https://example.com.

Fixture assumption: the website footer links Instagram, Facebook, TikTok, a marketplace listing, and a partner organization.

Required behavior:

- Inspect the website and follow or register the linked sources before asking for more URLs.
- Present the discovered inventory and ask the founder to confirm or correct it.
- Do not separately ask for social profiles, marketplace listings, or the linked partner.
- Offer private sources only as optional enrichment.

## Case 6: founder answer creates documentation gaps

Prompt sequence:

> We buy directly from certified-organic producers and collaborate with a conservation nonprofit.

Then answer one clarification with:

> We retain invoices and certificate copies, but I do not have them available now.

Required behavior:

- Record the operational statements as founder assertions with documentation pending.
- Register certificates, invoices, authorization, and impact proof as governance issues.
- Continue toward Identity rather than asking successive questions about every invoice, price calculation, legal structure, authorization scope, or measured outcome.
- Complete the initial interview within five questions and produce a draft with visible gaps.
- Offer a separate claim audit after the draft instead of silently beginning one.

## Scoring

Score each case from 0 to 2 on:

- Correct state detection
- Interactive mode selection
- One-question pacing
- Autonomous source discovery
- Validation-first questioning
- Bounded interview and closure
- Separation of identity work from claim auditing
- Concrete, evidence-derived wording
- Separation of evidence and decisions

A release candidate must score at least 16/18 in every applicable case and must have zero failure conditions from Case 1.

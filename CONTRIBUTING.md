# Contributing to Brand Soul

Brand Soul is an open-source framework created and maintained by [Cacao Web Studio](https://cacaowebstudio.com).

Contributions should improve evidence integrity, cross-agent portability, governance clarity, or measurable evaluation behavior. Avoid adding platform-specific marketing execution, generic branding advice, or files without a demonstrated reusable need.

## Before opening a pull request

1. Keep `brand-soul` as the technical Skill name.
2. Preserve the separation between Truth, Identity, Strategy, and Expression.
3. Add or update an eval case for behavioral changes.
4. Run:

   ```bash
   python3 evals/test_structural.py
   python3 scripts/validate_brand_repository.py assets/brand-repository-template
   ```

5. Confirm `SKILL.md` remains valid Agent Skills frontmatter and avoids vendor-only behavior.

By contributing, you agree that your contribution is licensed under Apache License 2.0.

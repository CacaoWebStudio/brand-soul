# Changelog

All notable Brand Soul changes are documented here. Versions follow Semantic Versioning.

## [Unreleased]

## [1.3.0] - 2026-09-02

### Added

- Mandatory Product Reality Inventory for product brands.
- Product-by-product catalog coverage checks before the identity interview.
- Regression evaluation for collections, product pages, variants, and product-level evidence.

### Changed

- Product facts are now extracted per item rather than collapsed into generic category descriptions.
- Product claims remain governed for downstream validation; catalog discovery itself does not trigger a claim audit.

## [1.2.0] - 2026-09-01

### Changed

- Existing-brand discovery now finds social profiles and other public sources from the website and public search before asking the founder for links.
- Source inventories are presented for confirmation or correction instead of being reconstructed manually by the founder.
- Initial founder interviews are limited to five identity-critical questions, with clarifications consuming the same budget.
- Brand Soul Build now records documentation gaps without turning automatically into an exhaustive claim audit.
- Sufficient answers close a topic; unresolved proof and operational details move to governance issues.
- Draft synthesis happens after the initial interview budget, with additional passes requiring the founder to opt in.

## [1.1.0] - 2026-09-01

### Added

- Cached, non-blocking checks for newer stable GitHub Releases.
- Safe interactive and opt-in automatic update commands.
- Guards against dirty installations, unofficial remotes, divergent history, and automatic major-version upgrades.
- Update-check and updater safety tests.

### Changed

- Brand Soul now reports an available stable update once per session when runtime and network access permit.
- Release and update instructions are documented for users and maintainers.

## [1.0.1] - 2026-09-01

### Changed

- Added interactive mode selection and separate existing-brand and new-brand Build paths.
- Changed founder discovery to one concrete question per turn.
- Made existing-brand discovery source-first, beginning with the primary website.
- Prohibited inferring brand maturity from an empty workspace or missing repository.

[Unreleased]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/CacaoWebStudio/brand-soul/releases/tag/v1.0.1

# Changelog

All notable Brand Soul changes are documented here. Versions follow Semantic Versioning.

## [Unreleased]

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

[Unreleased]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/CacaoWebStudio/brand-soul/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/CacaoWebStudio/brand-soul/releases/tag/v1.0.1

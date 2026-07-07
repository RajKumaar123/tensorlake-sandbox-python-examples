# Changelog

All notable changes to this project are documented in this file.

The format follows the principles of Keep a Changelog, and the project aims to follow Semantic Versioning where appropriate.

## [Unreleased]

### Added

- Complete set of 12 Tensorlake Sandbox examples
- Release candidate cleanup documentation
- Updated repository structure and quick start guidance

### Changed

- Documentation aligned with the completed repository state

### Fixed

- Broken or stale documentation references after moving docs into `docs/`

## [0.1.0] - Initial Development

### Added

#### Project Setup

- Created project repository
- Configured Python virtual environment
- Added `.env` support
- Configured API key loading

#### Tensorlake Sandbox

- Created first Tensorlake Sandbox
- Verified sandbox lifecycle
- Verified authentication
- Explored SDK APIs

#### Command Execution

- Executed Python commands inside sandbox
- Verified command execution
- Documented correct usage of `command` and `args`

#### Stateful Filesystem

- Created files inside sandbox
- Verified persistent filesystem
- Documented observations

#### Documentation

Added:

- README.md
- AGENTS.md
- ROADMAP.md
- notes.md
- CONTRIBUTING.md
- CHANGELOG.md

#### Engineering Discoveries

Verified:

- Sandbox creation
- Command execution
- Stateful filesystem
- SDK object structure

#### Repository

Created project structure:

```text
docs/
examples/
experiments/
utils/
```

## [0.2.0] - Example Expansion

### Added

- Package installation example
- Native file API example
- Snapshot example
- Supporting documentation for the first six examples

## [0.3.0] - Lifecycle and Process Workflows

### Added

- Suspend and resume example
- Process management example
- Documentation updates for advanced lifecycle workflows

## [0.4.0] - AI Workflow Examples

### Added

- Parallel sandboxes example
- Browser automation example
- Computer use example
- AI agent demo example

## Versioning Strategy

The project follows the following release strategy.

### Major Version

Breaking repository redesigns or significant architectural improvements.

Example:

```text
2.0.0
```

### Minor Version

New examples or major features.

Example:

```text
0.3.0
```

### Patch Version

Documentation improvements, bug fixes, and small enhancements.

Example:

```text
0.3.1
```

## Release Checklist

Before creating a new release, verify:

- Examples execute successfully
- Documentation updated
- Outputs verified
- notes.md updated
- ROADMAP.md updated
- README.md updated
- CHANGELOG.md updated

## Notes

This changelog is maintained manually.

Every meaningful change should be recorded here to preserve the development history of the project.

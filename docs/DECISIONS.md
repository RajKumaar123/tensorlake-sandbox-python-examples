# Architecture Decision Records

This document records the major architecture decisions for the flagship project.

## ADR-001 - Examples and flagship projects are separated

Examples remain in `examples/` as learning assets.
Flagship applications live under `projects/`.

## ADR-002 - Projects follow milestone-based development

The project must be built one milestone at a time with clear approval gates.

## ADR-003 - Tensorlake Sandbox is always the execution boundary

All sandboxed work must remain isolated behind a dedicated boundary.

## ADR-004 - Every milestone must compile before proceeding

No later milestone may begin until the current one is buildable and structurally sound.

## ADR-005 - Every milestone must execute successfully

Each milestone must have a runnable entrypoint or verification path.

## ADR-006 - Documentation is written alongside implementation

Documentation must evolve with the code, not after it.

## ADR-007 - Every milestone must be independently testable

Milestones must be small enough to verify on their own.

## ADR-008 - Reuse proven patterns from Examples 01-12

The flagship project should reuse verified repository patterns whenever appropriate.

## ADR-009 - Follow PEP 8 and modular architecture

The project should stay readable, modular, and maintainable.

## ADR-010 - Commit after every completed milestone

Every approved milestone should end with a Git commit.

## ADR-011 - Push every verified milestone to GitHub

Verified progress should be available in version control and shareable.

## ADR-012 - README is always kept current

The project README must reflect the actual repository state.

## ADR-013 - Project outputs must be reproducible

Artifacts should be generated in a way that can be repeated and reviewed.

## ADR-014 - Prefer composition over inheritance

Smaller composed parts are easier to reason about than deep class hierarchies.

## ADR-015 - Avoid premature optimization

Only optimize after a real need has been demonstrated.

## ADR-016 - Keep Tensorlake-specific logic isolated

SDK details should live behind clear abstractions.

## ADR-017 - Business logic must never depend directly on SDK implementation details

Application logic should rely on project interfaces and not on internal SDK assumptions.

## ADR-018 - Configuration must remain centralized

Runtime settings should be loaded from one clear configuration path.

## ADR-019 - Logging should be consistent across the project

Logging format and verbosity should be predictable across modules.

## ADR-020 - Architecture evolves incrementally

The project should improve in controlled, reviewable steps.

## ADR-021 - Artifact lifecycle must be explicit

Reports, logs, screenshots, and generated files must have a clear storage and retention strategy.

## ADR-022 - Testing and verification are required at every milestone

No milestone is complete without verification and test evidence.

## ADR-023 - Prompt management must be versioned

Prompts should be tracked as assets and updated deliberately.

## ADR-024 - Risky operations require cleanup and recovery planning

Long-running or persistent work must include termination and recovery behavior.

## ADR-025 - Keep the public interface simple

The top-level project surface should remain easy to navigate and explain.

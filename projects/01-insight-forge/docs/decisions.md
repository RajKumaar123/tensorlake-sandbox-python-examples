# Decisions

## Purpose

This file records the major architectural decisions for Tensorlake Intelligence Hub.

## Decisions So Far

### 1. Use a separate flagship project folder

Reason:

The repository already contains learning examples. A separate project keeps the flagship application distinct from the tutorial material.

### 2. Start with a thin foundation

Reason:

The project should be built milestone by milestone and remain independently testable at every stage.

### 3. Keep sandbox logic isolated

Reason:

Tensorlake interactions should be wrapped in a dedicated layer to improve maintainability and reduce duplication.

### 4. Use Markdown-first documentation

Reason:

The project is intended to support GitHub, Medium, and engineering review. Markdown keeps the repository transparent and easy to review.

## Open Questions

- Which persistence format will best support memory?
- How much should be stored locally versus in the sandbox?
- Which workflows should be automated first?

## Decision Rule

Any new subsystem should be added only after the current milestone is fully working and documented.

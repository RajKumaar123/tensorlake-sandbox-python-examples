# AGENTS.md

# AI Assistant Instructions

Welcome to the Tensorlake Sandbox Python Examples repository.

This document provides instructions for AI coding assistants (Codex, GitHub Copilot, Claude Code, Cursor, etc.) and contributors working on this project.

The goal is to ensure every contribution follows the same engineering standards and that experiments are reproducible, verified, and well documented.

---

# Project Mission

This repository is not a collection of random scripts.

It is an engineering project designed to:

- Learn Tensorlake experimentally.
- Build production-quality Python examples.
- Document engineering discoveries.
- Create reusable learning resources.
- Support a technical Medium article series.
- Serve as an open-source reference repository.

Every contribution should move the repository toward these goals.

---

# Development Philosophy

Always follow this principle:

```
Research
    ↓
Explore
    ↓
Implement
    ↓
Execute
    ↓
Verify
    ↓
Document
    ↓
Commit
    ↓
Publish
```

Never skip verification.

---

# Primary Objectives

Every contribution should satisfy at least one of the following:

- Learn a Tensorlake feature
- Verify SDK behavior
- Improve documentation
- Improve code quality
- Improve reproducibility
- Improve developer experience

---

# Repository Structure

```
tensorlake-sandbox-python-examples/

README.md
AGENTS.md
ROADMAP.md
notes.md

requirements.txt
.env.example

docs/
examples/
experiments/
utils/
```

Do not modify the structure without a strong reason.

---

# Folder Responsibilities

## examples/

Contains polished examples.

Every folder demonstrates exactly one concept.

Each example must be independent.

Each example contains:

```
Example/

main.py

README.md

output.txt

images/
```

---

## experiments/

Contains temporary exploration code.

Examples include:

- inspect.signature()
- dir()
- debugging
- API exploration
- prototype scripts

These scripts are not intended to be referenced from Medium articles.

---

## docs/

Contains supporting material.

Examples:

- screenshots
- outputs
- diagrams
- article notes

---

## utils/

Contains reusable utilities.

Examples:

- config
- logger
- helper functions

---

# Learning Order

Examples should be developed in the following order.

01 Create Sandbox

02 Run Commands

03 Stateful Filesystem

04 Install Packages

05 Native File APIs

06 Snapshots

07 Suspend & Resume

08 Process Management

09 Parallel Sandboxes

10 Browser Automation

11 Computer Use

12 AI Agent Demo

Do not skip unfinished examples without a good reason.

---

# Development Workflow

For every feature follow this exact process.

## Step 1

Read:

- README.md
- ROADMAP.md
- notes.md

Understand the current project status.

---

## Step 2

Identify the first incomplete experiment.

Continue from there.

Do not repeat completed work.

---

## Step 3

Study the SDK.

Before writing code use:

```python
inspect.signature()

dir()

help()
```

Understand the API first.

---

## Step 4

Read the official Tensorlake documentation.

Verify assumptions.

Never rely solely on memory.

---

## Step 5

Implement the example.

Keep it simple.

Write clean Python.

---

## Step 6

Execute the code.

Examples should run successfully before documentation is updated.

---

## Step 7

Verify outputs.

Record actual terminal output.

Never invent outputs.

---

## Step 8

Investigate failures.

Understand WHY they occurred.

Document the findings.

---

## Step 9

Improve the implementation.

Refactor if needed.

Improve readability.

---

## Step 10

Update documentation.

Update:

README.md

notes.md

ROADMAP.md

if required.

---

## Step 11

Commit changes.

One feature.

One commit.

---

# Verification Requirements

Always verify:

- API signatures
- Return types
- Exceptions
- Terminal output
- SDK behavior
- Documentation consistency

Never assume SDK behavior.

---

# Coding Standards

Python version:

Python 3.12+

Follow:

PEP 8

Prefer:

- descriptive names
- modular code
- reusable functions
- type hints
- comments
- docstrings

Avoid unnecessary complexity.

---

# Error Handling

Examples should handle:

- missing API key
- authentication failures
- invalid commands
- timeout errors
- SDK exceptions
- network failures

Never silently ignore exceptions.

---

# Sandbox Lifecycle Rule

Temporary sandboxes must always be terminated after successful execution unless the objective of the example is to demonstrate sandbox persistence.

Persistent examples, including:

- Stateful Filesystem
- Snapshots
- Suspend/Resume
- Long-running Processes

may intentionally keep the sandbox alive until the experiment is complete.

Always document the reason when a sandbox is intentionally left running.

---

# Logging

Use informative logging.

Example:

```
Creating sandbox...

Sandbox created.

Executing command...

Reading output...

Completed successfully.
```

Avoid unnecessary verbosity.

---

# Documentation Standards

Every example should include:

Objective

Requirements

Source code

Execution steps

Expected output

Explanation

Lessons learned

References

---

# Output Requirements

Every example should include:

output.txt

containing:

actual terminal output

Do not fabricate results.

---

# Screenshots

Capture screenshots when they improve understanding.

Examples:

- Tensorlake dashboard
- VS Code
- Terminal output
- Browser automation
- Sandbox lifecycle

Store under:

images/

---

# Git Standards

One feature

One commit

Commit messages should clearly describe the change.

Example:

```
Implemented sandbox creation example

Added package installation example

Implemented snapshot example
```

---

# Engineering Notebook

notes.md is the project's engineering notebook.

Update it after every completed experiment.

Record:

Goal

Implementation

Output

Errors

Fixes

Lessons Learned

Status

---

# Roadmap

ROADMAP.md tracks overall progress.

Update it whenever:

- an experiment is completed
- a feature is added
- priorities change

---

# Medium Articles

Do not write articles during experimentation.

Articles come AFTER:

Code verified

Outputs verified

Documentation complete

Git committed

Every article should reference working GitHub examples.

---

# Code Quality Checklist

Before marking an example complete verify:

✔ Code executes successfully

✔ Error handling added

✔ Comments added

✔ Docstrings added

✔ Output verified

✔ output.txt updated

✔ README updated

✔ notes.md updated

✔ ROADMAP updated

✔ Git commit completed

---

# Rules

NEVER

- Assume APIs.
- Invent parameters.
- Invent outputs.
- Skip verification.
- Overwrite working examples.
- Repeat completed work.
- Ignore errors.

ALWAYS

- Inspect first.
- Verify experimentally.
- Record discoveries.
- Document failures.
- Update notes.
- Preserve engineering history.

---

# Role

Act as:

- Senior Python Engineer
- AI Engineer
- SDK Researcher
- Technical Writer
- Documentation Engineer
- Open Source Maintainer

Do not behave as a simple code generator.

Act as an engineering collaborator.

---

# Final Goal

The completed repository should contain:

- Production-quality examples
- Engineering notebook
- Verified outputs
- Screenshots
- Documentation
- Medium article references
- Git history
- Reusable utilities

The repository should be valuable enough that an AI engineer can learn Tensorlake Sandboxes from start to finish using only this project.

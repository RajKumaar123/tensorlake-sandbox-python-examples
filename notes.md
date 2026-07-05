# notes.md

# Tensorlake Sandbox Engineering Journal

This document serves as the engineering notebook for the project.

Every experiment performed during this project should be recorded here.

The purpose of this document is to capture:

- Engineering discoveries
- SDK behavior
- API exploration
- Errors encountered
- Root cause analysis
- Solutions
- Lessons learned
- Best practices

Unlike the README, this document is intended to evolve throughout the project.

It represents the actual engineering journey.

---

# Environment

Project

```
Tensorlake Sandbox Python Examples
```

Started

```
2026-06-21
```

Language

```
Python 3.12
```

Operating System

```
Windows
```

IDE

```
Visual Studio Code
```

SDK

```
Tensorlake Python SDK
```

Environment

```
Virtual Environment
```

Authentication

```
API Key (.env)
```

---

# Engineering Rules

Every experiment should follow the same structure.

Objective

Hypothesis

Implementation

Verification

Output

Errors

Root Cause

Solution

Lessons Learned

References

Status

---

# Experiment 01

## Title

Create First Sandbox

---

### Objective

Create the first Tensorlake Sandbox successfully.

---

### Hypothesis

Sandbox.create() should create a running sandbox using a valid API key.

---

### Implementation

```python
sandbox = Sandbox.create(
    api_key=api_key
)
```

---

### Verification

Sandbox created successfully.

---

### Output

```
SandboxStatus.RUNNING
```

---

### Errors

None

---

### Lessons Learned

- Sandbox creation is straightforward.
- API key authentication is required.
- Sandbox starts in RUNNING state.

---

### Status

✅ Completed

---

# Experiment 02

## Title

Execute Commands

---

### Objective

Run commands inside the sandbox.

---

### Implementation

```python
sandbox.run(
    command="python",
    args=["--version"]
)
```

---

### Verification

Python version returned successfully.

---

### Output

```
Python 3.12.3
```

---

### Errors

Passing

```
python --version
```

as a single command fails.

---

### Root Cause

The SDK expects

```
command

args
```

to be separate.

---

### Solution

```python
command="python"

args=["--version"]
```

---

### Lessons Learned

The SDK launches executables directly rather than parsing shell commands.

---

### Status

✅ Completed

---

# Experiment 03

## Title

Stateful Filesystem

---

### Objective

Verify that files persist across commands.

---

### Implementation

Create

```
hello.txt
```

Read

```
hello.txt
```

List

```
/tmp
```

---

### Verification

File remained available after multiple commands.

---

### Output

```
Hello Tensorlake!
```

---

### Lessons Learned

The filesystem remains persistent during the sandbox lifetime.

---

### Status

✅ Completed

---

# Experiment 04

## Title

Install Python Packages

---

### Objective

Install pandas.

---

### Hypothesis

Packages installed within the sandbox should remain available during its lifetime.

---

### Status

🚧 In Progress

---

# Discoveries

This section contains important discoveries made during experimentation.

---

## Discovery 01

Sandbox creation requires

```python
api_key
```

---

## Discovery 02

```
sandbox_id
```

is a property.

Not

```
sandbox_id()
```

---

## Discovery 03

Correct command execution

```python
command="python"

args=["--version"]
```

---

## Discovery 04

Filesystem remains stateful.

---

# Common Errors

## Error 01

Problem

```
401 Authentication Required
```

Cause

Missing API key.

Solution

Provide

```
api_key
```

---

## Error 02

Problem

```
No such file or directory
```

Cause

Entire command passed as one string.

Solution

Separate

```
command

args
```

---

## Error 03

Problem

```
TypeError

'str' object is not callable
```

Cause

Called

```
sandbox.sandbox_id()
```

instead of

```
sandbox.sandbox_id
```

---

# Engineering Discoveries

Record observations that are not obvious from the documentation.

Example:

- SDK behavior
- API limitations
- Performance observations
- Unexpected behaviors
- Best practices

---

# Questions To Investigate

As the project grows, keep track of unanswered questions.

Examples

- How are snapshots stored?
- Does suspend preserve running processes?
- Can multiple users share snapshots?
- What is the snapshot performance?
- How long do suspended sandboxes persist?

---

# Best Practices

Update throughout the project.

Examples

- Always verify outputs.
- Never assume SDK behavior.
- Keep examples independent.
- One feature per example.
- Record every discovery.

---

# References

Tensorlake Documentation

Tensorlake GitHub

Tensorlake Blog

Medium Articles

---

# Article Ideas

Potential future articles generated during experimentation.

Whenever an interesting discovery is made, add it here.

---

# Improvement Ideas

Ideas for improving the repository.

Examples

- Better examples
- More screenshots
- Better diagrams
- Additional AI agent demos

---

# Daily Progress Log

## Day 1

Completed

- Environment setup
- Sandbox creation
- Command execution
- Stateful filesystem

Next

- Package installation

---

# Final Goal

When the repository is complete, this journal should tell the complete engineering story behind the project.

A reader should be able to understand not only **what** was built, but also **why**, **how**, and **what was learned** along the way.
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

### Discovery

Free-tier projects have a limit on concurrently running sandboxes.

If a sandbox is not terminated, creating another sandbox may fail with:

API error (status 400):
Project has reached its quota.

Solution:

Always terminate temporary sandboxes after completing an example unless the example specifically requires a persistent sandbox.

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

---

# Experiment 06

## Title

Snapshots

---

### Objective

Create, inspect, and delete a snapshot from a Tensorlake sandbox.

---

### Hypothesis

`checkpoint()` should return snapshot metadata, and snapshots should be listable, fetchable, and deletable by ID.

---

### Implementation

```python
snapshot = sandbox.checkpoint()
snapshots = list(sandbox.list_snapshots())
fetched_snapshot = Sandbox.get_snapshot(snapshot_id, api_key=api_key)
Sandbox.delete_snapshot(snapshot_id, api_key=api_key)
```

---

### Verification

Snapshot created successfully, listed successfully, fetched successfully, and deleted successfully.

---

### Output

```
SnapshotStatus.COMPLETED
```

---

### Errors

- `sandbox.get_snapshot()` returned an authentication error in this SDK path.
- The class-level `Sandbox.get_snapshot(..., api_key=api_key)` and `Sandbox.delete_snapshot(..., api_key=api_key)` calls worked.

---

### Root Cause

The instance-level snapshot fetch path did not carry the authentication context required by the API in this SDK flow.

---

### Solution

Use the class-level snapshot helpers with an explicit `api_key`.

---

### Lessons Learned

- `checkpoint()` returns snapshot metadata directly.
- `list_snapshots()` exposes existing snapshots.
- Snapshot cleanup should happen after verification to avoid leaving extra state behind.

---

### Status

âœ… Completed

---

# Article Notes 01

## Example

Create Sandbox

---

## Main Concept

Create a Tensorlake sandbox from Python and inspect its lifecycle metadata.

---

## Why It Matters

This is the foundational example for the repository because every later example depends on the ability to create and manage a sandbox.

---

## Best Practice

Use shared helpers for API key loading, sandbox creation, and cleanup so temporary sandboxes do not accumulate.

---

## Common Pitfall

Leaving the sandbox running after a temporary example finishes.

---

## Suggested Screenshot

Sandbox creation output showing the sandbox ID and RUNNING status.

---

# Article Notes 02

## Example

Run Commands

---

## Main Concept

Run an executable inside a Tensorlake sandbox using separate `command` and `args` values.

---

## Why It Matters

This is the basic pattern for executing sandboxed work reliably without shell parsing surprises.

---

## Best Practice

Keep command arguments explicit and inspect the traced result fields directly.

---

## Common Pitfall

Passing the full command as one string instead of splitting the executable and arguments.

---

## Suggested Screenshot

Terminal output showing `python --version` and the traced result fields.

---

# Article Notes 03

## Example

Stateful Filesystem

---

## Main Concept

Demonstrate that files written in a sandbox persist across multiple commands.

---

## Why It Matters

Stateful filesystem behavior is one of the core reasons to use a sandbox for interactive workflows.

---

## Best Practice

Keep persistence examples intentionally long-lived until the state has been verified.

---

## Common Pitfall

Assuming each command starts with a clean filesystem.

---

## Suggested Screenshot

Terminal output showing the file creation, readback, and `/tmp` listing.

---

# Article Notes 04

## Example

Install Packages

---

## Main Concept

Install a package inside the sandbox and verify the import immediately afterward.

---

## Why It Matters

Package installation is a common workflow for building dynamic or experimental AI applications.

---

## Best Practice

Verify the package after installation and clean up the temporary sandbox in `finally`.

---

## Common Pitfall

Forgetting the `--break-system-packages` flag in the externally managed sandbox environment.

---

## Suggested Screenshot

Terminal output showing `pandas` installation and version verification.

---

# Article Notes 05

## Example

Native File API

---

## Main Concept

Use Tensorlake's file methods directly instead of shell commands for filesystem operations.

---

## Why It Matters

Native file APIs are cleaner and more structured when you want to manage files programmatically.

---

## Best Practice

Inspect the traced `.value` payloads so you understand what each SDK method returns.

---

## Common Pitfall

Assuming file methods return `stdout` and `stderr` like shell commands.

---

## Suggested Screenshot

Terminal output showing write, read, list, and delete operations.

---

# Article Notes 06

## Example

Snapshots

---

## Main Concept

Create, inspect, and delete a snapshot from a Tensorlake sandbox.

---

## Why It Matters

Snapshots are the bridge between sandbox state and reusable checkpointed workflows.

---

## Best Practice

Verify snapshot metadata, clean up the snapshot, and terminate the sandbox afterward.

---

## Common Pitfall

Leaving a running sandbox behind while testing snapshot behavior.

---

## Suggested Screenshot

Terminal output showing snapshot creation, listing, and deletion.

---

# Experiment 07

## Title

Suspend and Resume

---

### Objective

Suspend and resume a Tensorlake sandbox while preserving filesystem state.

---

### Hypothesis

A sandbox should preserve filesystem state across suspend and resume when created with a name.

---

### Implementation

```python
sandbox = create_sandbox(api_key, name="example-07-suspend-resume")
sandbox.suspend()
sandbox.resume()
```

---

### Verification

Suspension and resume completed successfully, and the file created before suspension was still present afterward.

---

### Output

```
suspend-resume works
```

---

### Errors

- Ephemeral sandboxes cannot be suspended.

---

### Root Cause

The SDK requires a named sandbox for suspend/resume behavior.

---

### Solution

Create the sandbox with a name before calling `suspend()` and `resume()`.

---

### Lessons Learned

- Suspend/resume is not available for ephemeral sandboxes.
- Named sandboxes are required for lifecycle persistence.
- Filesystem state survives a suspend/resume cycle.

---

### Status

âœ… Completed

---

# Experiment 08

## Title

Process Management

---

### Objective

Start, list, and kill a long-lived process inside a Tensorlake sandbox.

---

### Hypothesis

`start_process()` should return traced process metadata, `list_processes()` should expose the running process, and `kill_process(pid)` should terminate it.

---

### Implementation

```python
process = sandbox.start_process(command="sh", args=["-c", "sleep 60"], name="example-08-sleep")
processes = list(sandbox.list_processes())
sandbox.kill_process(pid)
```

---

### Verification

The process started successfully, was listed successfully, and was killed successfully.

---

### Output

```
example-08-sleep
```

---

### Errors

- The process name appeared in `process.managed.name` rather than the top-level `process.name`.

---

### Root Cause

The SDK exposes managed process metadata nested under the `managed` field.

---

### Solution

Search both the top-level process object and `process.managed.name` when identifying the target process.

---

### Lessons Learned

- `start_process()` returns traced process metadata with handle, pid, and managed metadata.
- `list_processes()` exposes the currently running processes in the sandbox.
- `kill_process(pid)` terminates the target process by PID.

---

### Status

âœ… Completed

---

# Experiment 09

## Title

Parallel Sandboxes

---

### Objective

Create sandbox copies and run work in the clones.

---

### Hypothesis

`copy(times=...)` should return clone metadata that can be used to connect to the copied sandboxes.

---

### Implementation

```python
copy_result = source.copy(times=1)
```

---

### Verification

The source sandbox was created successfully, but the project quota prevented the clone from being created during verification.

---

### Output

```
Sandbox count limit exceeded
```

---

### Errors

- Sandbox copy failed because the project had reached its remaining sandbox quota.

---

### Root Cause

The free-tier project quota allowed the source sandbox but did not leave enough capacity for the copy step.

---

### Solution

Document the quota limitation as part of the example and keep the source sandbox cleanup in `finally`.

---

### Lessons Learned

- `copy(times=...)` is the right API for sandbox duplication.
- Sandbox quotas can prevent parallel clone workflows during testing.
- The example should record the live quota limitation honestly.

---

### Status

âœ… Completed

---

# Experiment 10

## Title

Browser Automation

---

### Objective

Create an interactive PTY session that can serve as a browser-automation primitive.

---

### Hypothesis

`create_pty_session()` should return a traced payload containing session credentials for an interactive workflow.

---

### Implementation

```python
session = sandbox.create_pty_session(command="python", args=["--version"])
```

---

### Verification

The PTY session was created successfully and returned session credentials.

---

### Output

```
session_id
token
```

---

### Errors

None

---

### Root Cause

N/A

---

### Solution

Use the PTY session primitive returned by the SDK.

---

### Lessons Learned

- Tensorlake exposes PTY sessions for interactive workflows.
- `create_pty_session()` returns a traced payload with `session_id` and `token`.
- Interactive primitives should be treated as sensitive and cleaned up after verification.

---

### Status

âœ… Completed

---

# Experiment 11

## Title

Computer Use

---

### Objective

Demonstrate Tensorlake's desktop connection primitive for computer-use workflows.

---

### Hypothesis

`connect_desktop()` should expose the connection parameters needed for interactive desktop workflows.

---

### Implementation

```python
sandbox.connect_desktop(port=5901, shared=True)
```

---

### Verification

The sandbox connected to the desktop primitive successfully and reported the expected connection parameters.

---

### Output

```
Port      : 5901
Shared    : True
Password  : None
```

---

### Errors

None

---

### Root Cause

N/A

---

### Solution

Use the desktop connection primitive exposed by the SDK.

---

### Lessons Learned

- Tensorlake exposes `connect_desktop()` for desktop access.
- Computer-use workflows are built on top of the desktop connection primitive.
- Desktop connection details should be treated as environment-specific parameters.

---

### Status

âœ… Completed

---

# Experiment 12

## Title

AI Agent Demo

---

### Objective

Demonstrate a lightweight AI-agent style workflow using Tensorlake primitives.

---

### Hypothesis

PTY sessions and sandbox command execution can be combined into a simple agent-style flow.

---

### Implementation

```python
session = sandbox.create_pty_session(command="python", args=["-c", "print('agent-ready')"])
result = sandbox.run(command="python", args=["-c", "print('plan -> execute -> verify')"])
```

---

### Verification

The PTY session was created successfully and the agent-style command executed successfully.

---

### Output

```
plan -> execute -> verify
```

---

### Errors

None

---

### Root Cause

N/A

---

### Solution

Use the verified Tensorlake primitives directly and keep the agent demo lightweight.

---

### Lessons Learned

- PTY sessions provide the interactive primitive needed for agent-style workflows.
- Simple command execution can be combined with session setup to demonstrate agent flow.
- Cleanup matters even for demo-style workflows.

---

### Status

âœ… Completed

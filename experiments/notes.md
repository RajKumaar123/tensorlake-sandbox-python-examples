# Tensorlake Sandbox Exploration Notes

This file records experiments, outputs, discoveries, errors, fixes, and lessons learned.

---

# Purpose

This repository is a hands-on exploration of Tensorlake Sandboxes.

Goals:

- Learn Tensorlake experimentally.
- Verify APIs before using them.
- Avoid assumptions.
- Build production-quality examples.
- Document discoveries.
- Generate material for technical articles.
- Enable Codex to continue exploration without repeating work.

---

# Environment

Date Started

```
2026-06-21
```

Python Version

```
Python 3.12.5
```

Packages

```
tensorlake
python-dotenv
```

Virtual Environment

```
Activated
```

API Key

```
Stored in .env
```

Variable Name

```env
TENSORLAKE_API_KEY
```

Default API URL

```
https://api.tensorlake.ai
```

---

# Current Project Structure

```
tensorlake/
│
├── .env
├── requirements.txt
├── README.md
├── notes.md
│
├── create_sandbox.py
├── run_commands.py
├── stateful_sandbox.py
├── install_packages.py
├── file_operations.py
├── snapshots.py
├── suspend_resume.py
├── process_management.py
├── fork_sandbox.py
├── pty_sessions.py
├── desktop_mode.py
└── agent_demo.py
```

---

# Experiment Template

Every experiment should follow:

Goal

Code

Output

Result

Lessons Learned

Status

---

# Experiment 1: Sandbox Creation

Goal

Create the first Tensorlake sandbox.

Code

```python
sandbox = Sandbox.create(
    api_key=api_key
)
```

Example Output

```
Sandbox ID : d270a6uhxj4vqrkmy0t7a
Status     : SandboxStatus.RUNNING
```

Result

SUCCESS

Notes

- Sandbox creation successful.
- Sandbox status becomes RUNNING.

Lessons Learned

Correct:

```python
sandbox.sandbox_id
```

Wrong:

```python
sandbox.sandbox_id()
```

Status

✅ Completed

---

# Experiment 2: Execute Commands

Goal

Execute commands inside the sandbox.

Code

```python
result = sandbox.run(
    command="python",
    args=["--version"]
)
```

Output

```
Python 3.12.3
```

Result

SUCCESS

Lessons Learned

Wrong:

```python
sandbox.run(
    command="python --version"
)
```

Error

```
No such file or directory
```

Correct

```python
sandbox.run(
    command="python",
    args=["--version"]
)
```

Status

✅ Completed

---

# Experiment 3: Understand Command Result Object

Goal

Understand the return object.

Correct

```python
result.exit_code
result.stdout
result.stderr
result.trace_id
```

Wrong

```python
result.result.exit_code
```

Result

SUCCESS

Status

✅ Completed

---

# Experiment 4: Stateful Filesystem

Goal

Create and read files.

Create

```python
sandbox.run(
    command="sh",
    args=["-c", "echo 'Hello Tensorlake!' > /tmp/hello.txt"]
)
```

Read

```python
sandbox.run(
    command="cat",
    args=["/tmp/hello.txt"]
)
```

Output

```
Hello Tensorlake!
```

List

```python
sandbox.run(
    command="ls",
    args=["-l", "/tmp"]
)
```

Example Output

```
-rw-r--r-- hello.txt
```

Result

SUCCESS

Lessons Learned

Filesystem state persists across commands.

Status

✅ Completed

---

# Experiment 5: Install pandas

Goal

Install pandas inside sandbox.

Status

⬜ Not Started

Notes

None

---

# Experiment 6: Verify pandas

Goal

Verify pandas installation.

Status

⬜ Not Started

Notes

None

---

# Experiment 7: Native File APIs

Functions

```python
sandbox.write_file()
sandbox.read_file()
sandbox.list_directory()
sandbox.delete_file()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 8: Snapshots

Functions

```python
sandbox.checkpoint()
sandbox.list_snapshots()
sandbox.get_snapshot()
sandbox.delete_snapshot()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 9: Suspend and Resume

Functions

```python
sandbox.suspend()
sandbox.resume()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 10: Process Management

Functions

```python
sandbox.start_process()
sandbox.list_processes()
sandbox.kill_process()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 11: Forking

Functions

```python
sandbox.copy()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 12: PTY Sessions

Functions

```python
sandbox.create_pty()
sandbox.connect_pty()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 13: Desktop Mode

Functions

```python
sandbox.connect_desktop()
```

Status

⬜ Not Started

Notes

None

---

# Experiment 14: AI Agent Demo

Architecture

```
User
↓
LLM
↓
Tensorlake Sandbox
↓
Python Tools
↓
Filesystem
↓
Persistent State
```

Status

⬜ Not Started

Notes

None

---

# Current Task

Current Active Experiment

```
Experiment 5
```

Task

```
Install pandas inside sandbox
```

Status

```
ACTIVE
```

---

# Global Discoveries

Default API URL

```
https://api.tensorlake.ai
```

Sandbox Creation

```python
Sandbox.create(api_key=api_key)
```

Command Execution

Wrong

```python
sandbox.run(
    command="python --version"
)
```

Correct

```python
sandbox.run(
    command="python",
    args=["--version"]
)
```

Result Object

Correct

```python
result.exit_code
result.stdout
result.stderr
result.trace_id
```

Wrong

```python
result.result.exit_code
```

Sandbox Properties

Correct

```python
sandbox.sandbox_id
sandbox.status
```

Wrong

```python
sandbox.sandbox_id()
sandbox.status()
```

Statefulness

Supported

Filesystem

Persistent

---

# Error Log

## Error 1

Problem

```python
sandbox.run(
    command="python --version"
)
```

Error

```
No such file or directory
```

Fix

```python
sandbox.run(
    command="python",
    args=["--version"]
)
```

---

## Error 2

Problem

```python
result.result.exit_code
```

Error

```
AttributeError
```

Fix

```python
result.exit_code
result.stdout
result.stderr
result.trace_id
```

---

## Error 3

Problem

```python
sandbox.sandbox_id()
```

Error

```
TypeError: 'str' object is not callable
```

Fix

```python
sandbox.sandbox_id
```

---

## Error 4

Problem

```python
Sandbox.create()
```

Error

```
401 Authentication required
```

Fix

```python
Sandbox.create(
    api_key=api_key
)
```

---

# Verification Requirements

For every experiment:

1. Verify APIs before using them.
2. Use inspect.signature().
3. Use dir().
4. Use docstrings.
5. Verify return types.
6. Verify outputs experimentally.
7. Compare findings with Tensorlake documentation.
8. Record errors and fixes.
9. Update notes.md.
10. Never assume APIs.

---

# Success Workflow

When an experiment succeeds:

1. Mark it completed.
2. Record output.
3. Record discoveries.
4. Record lessons learned.
5. Update notes.md.
6. Never overwrite working files.
7. Create one file per experiment.
8. Preserve previous successful experiments.

---

# Rules

NEVER

- Assume APIs.
- Invent parameters.
- Repeat completed experiments.
- Overwrite working files.
- Ignore failures.
- Hallucinate behavior.

ALWAYS

- Inspect APIs first.
- Verify experimentally.
- Record outputs.
- Record errors.
- Explain failures.
- Create one file per experiment.
- Update notes.md.
- Prefer discovery over assumptions.

---

# Instructions For Codex

Before writing code:

1. Read README.md.
2. Read notes.md.
3. Understand completed experiments.
4. Continue only from the first incomplete experiment.
5. Verify APIs before using them.
6. Use:

```python
inspect.signature()
dir()
help()
```

7. Validate outputs experimentally.
8. Record discoveries.
9. Record failures and fixes.
10. Update notes.md after every successful experiment.
11. Never overwrite working files.
12. Create one file per experiment.
13. Generate production-quality code with:
    - comments
    - docstrings
    - logging
    - error handling

Act like:

- Senior Python Engineer
- SDK Researcher
- Documentation Engineer
- Technical Writer

Discover first.
Verify second.
Code third.
Document fourth.

Never hallucinate APIs.
Always validate experimentally.
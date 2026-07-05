# Tensorlake Sandbox Exploration

A hands-on exploration of Tensorlake Sandboxes using Python.

Goal:

- Learn Tensorlake Sandbox APIs experimentally.
- Build reproducible examples.
- Document findings.
- Produce production-quality code.
- Create material for technical articles.

---

# Environment

Python Version

```
Python 3.12.5
```

Virtual Environment

```
Activated
```

Packages

```txt
tensorlake
python-dotenv
```

API Key

Stored in:

```env
.env
```

Variable:

```env
TENSORLAKE_API_KEY
```

---

# Project Structure

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

# Completed Tasks

## Environment Setup

- [x] Create virtual environment
- [x] Install tensorlake
- [x] Install python-dotenv
- [x] Configure .env

---

## Sandbox Creation

Code:

```python
sandbox = Sandbox.create(api_key=api_key)
```

Status

✅ Completed

---

## Command Execution

Code:

```python
result = sandbox.run(
    command="python",
    args=["--version"]
)
```

Output:

```
Python 3.12.3
```

Status

✅ Completed

---

## Stateful Filesystem

Create file:

```python
sandbox.run(
    command="sh",
    args=["-c", "echo 'Hello Tensorlake!' > /tmp/hello.txt"]
)
```

Read file:

```python
sandbox.run(
    command="cat",
    args=["/tmp/hello.txt"]
)
```

Output:

```
Hello Tensorlake!
```

List:

```python
sandbox.run(
    command="ls",
    args=["-l", "/tmp"]
)
```

Status

✅ Completed

---

# Important Discoveries

## Sandbox Creation

Correct:

```python
Sandbox.create(api_key=api_key)
```

---

## API URL

Default:

```python
https://api.tensorlake.ai
```

No need to specify.

---

## sandbox_id

Correct:

```python
sandbox.sandbox_id
```

Wrong:

```python
sandbox.sandbox_id()
```

---

## Command Execution

Wrong:

```python
sandbox.run(
    command="python --version"
)
```

Correct:

```python
sandbox.run(
    command="python",
    args=["--version"]
)
```

---

## Result Object

Correct:

```python
result.exit_code
result.stdout
result.stderr
result.trace_id
```

Wrong:

```python
result.result.exit_code
```

---

# Remaining Experiments

## Package Installation

- [ ] Install pandas
- [ ] Verify pandas
- [ ] Install numpy
- [ ] Verify numpy

---

## Native File APIs

Explore:

```python
sandbox.write_file()
sandbox.read_file()
sandbox.list_directory()
sandbox.delete_file()
```

---

## Snapshots

Explore:

```python
sandbox.checkpoint()
sandbox.list_snapshots()
sandbox.get_snapshot()
sandbox.delete_snapshot()
```

---

## Suspend and Resume

Explore:

```python
sandbox.suspend()
sandbox.resume()
```

---

## Process Management

Explore:

```python
sandbox.start_process()
sandbox.list_processes()
sandbox.kill_process()
```

---

## Forking

Explore:

```python
sandbox.copy()
```

---

## PTY Sessions

Explore:

```python
sandbox.create_pty()
sandbox.connect_pty()
```

---

## Desktop Mode

Explore:

```python
sandbox.connect_desktop()
```

---

## AI Agent Demo

Architecture

```
User
 ↓
LLM
 ↓
Tensorlake Sandbox
 ↓
Filesystem
 ↓
Persistent State
```

---

# Verification Requirements

For every experiment:

1. Inspect APIs first.
2. Verify signatures.
3. Verify return types.
4. Verify outputs.
5. Compare with documentation.
6. Document findings.
7. Record failures.
8. Explain lessons learned.
9. Update notes.md.
10. Never assume behavior.

---

# Rules

NEVER

- Assume APIs.
- Invent parameters.
- Repeat completed tasks.
- Overwrite working files.
- Ignore errors.

ALWAYS

- Use inspect.signature()
- Use dir()
- Use docstrings
- Verify experimentally
- Record outputs
- Create one file per experiment
- Update notes.md
- Explain failures

---

# Instructions For Codex

Read:

1. README.md
2. notes.md

Before writing code.

DO NOT repeat completed tasks.

Continue from the first incomplete experiment.

Verify assumptions before coding.

Generate:

- production-quality code
- comments
- docstrings
- error handling
- logging

When an experiment succeeds:

1. Create a new file.
2. Update notes.md.
3. Mark task complete.
4. Add discoveries.
5. Record outputs.

Act like a senior Python engineer and research collaborator.
# Example 02: Run Commands

This example shows how to run a command inside a Tensorlake sandbox and inspect the traced result object.

## Overview

This example demonstrates the command execution flow:

1. Load credentials.
2. Create a temporary sandbox.
3. Execute a command with separate arguments.
4. Read the traced command result.
5. Terminate the sandbox.

## Objective

Create a sandbox, run `python --version`, and print the command output and metadata.

## Prerequisites

- Python 3.12+
- `tensorlake`
- `python-dotenv`
- A valid `TENSORLAKE_API_KEY` in `.env`

## Project Structure

- `main.py`
- `output.txt`

## How to Run

```bash
python examples/02_run_commands/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` executes `python --version` with `command` and `args` separated.
3. The traced result exposes the command metadata and output.
4. The sandbox is terminated because this is a temporary example.

## Expected Output

The script should print the Python version returned by the sandbox.

The exact trace ID may differ between runs.

## Key Learnings

- The SDK expects commands and arguments separately.
- The traced result object exposes `trace_id`, `exit_code`, `stdout`, and `stderr`.
- Temporary sandboxes must be cleaned up after execution.

## Common Pitfalls

- Passing `python --version` as a single command string
- Forgetting to terminate a temporary sandbox
- Assuming a trace ID will be stable across runs

## Best Practices

- Use shared helpers from `utils/common.py`.
- Keep command execution explicit and readable.
- Always verify and record the live output.

## Notes

- The command and arguments are passed separately.
- The result object exposes `trace_id`, `exit_code`, `stdout`, and `stderr`.
- The sandbox is intentionally terminated at the end because this example uses a temporary sandbox.

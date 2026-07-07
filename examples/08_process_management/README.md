# Example 08: Process Management

This example demonstrates how to start, list, and kill a process inside a Tensorlake sandbox.

## Overview

This example walks through the process-management lifecycle:

1. Load credentials.
2. Create a sandbox.
3. Start a long-lived process.
4. List the running processes.
5. Kill the target process.
6. Clean up the sandbox.

## Objective

Launch a process, inspect it, and terminate it from inside Tensorlake.

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
python examples/08_process_management/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` starts a `sleep` process with a stable name.
3. The example lists processes and finds the target process by name.
4. The target process is killed by PID.
5. The sandbox is terminated in `finally`.

## Expected Output

The script should show the process starting, the process list, and the process being killed successfully.

## Key Learnings

- `start_process()` returns traced process metadata.
- `list_processes()` exposes the currently running sandbox processes.
- `kill_process(pid)` terminates the target process by PID.

## Common Pitfalls

- Assuming `start_process()` returns a shell-style command output
- Failing to use a stable process name when searching the process list
- Leaving a temporary sandbox open after the test

## Best Practices

- Name the process so it can be found in the process list.
- Clean up the process before terminating the sandbox.
- Use the shared helpers in `utils/common.py`.

## Notes

- This example uses `sleep 60` to create a simple long-lived process for demonstration.
- The sandbox is terminated after the process-management workflow completes.

# Example 03: Stateful Filesystem

This example shows that files created inside a Tensorlake sandbox persist across commands.

## Overview

This example demonstrates filesystem persistence inside the sandbox:

1. Load credentials.
2. Create a sandbox.
3. Write a file.
4. Read the file back.
5. List the directory to confirm the file remains present.

## Objective

Create a file, read it back, and list the sandbox filesystem to confirm persistence.

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
python examples/03_stateful_filesystem/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` writes `/tmp/hello.txt` with `sh`.
3. The example reads the file back with `cat`.
4. The example lists `/tmp` to confirm the file remains in the filesystem.
5. The sandbox is intentionally left running because persistence is the lesson.

## Expected Output

The script should show the file being created, read, and listed in the sandbox filesystem.

The sandbox is intentionally left running because persistence is the behavior being demonstrated.

## Key Learnings

- Files created in the sandbox persist across commands.
- The filesystem state can be reused later in the same sandbox session.
- Persistence examples should not auto-clean up before the learning objective is complete.

## Common Pitfalls

- Assuming each command runs in a fresh filesystem
- Cleaning up a sandbox before verifying persistence
- Forgetting that this example is intentionally long-lived

## Best Practices

- Keep persistence examples clearly documented.
- Leave the sandbox running only when persistence is the objective.
- Use the shared helpers for consistent setup behavior.

## Notes

- This is a persistence example, so it does not automatically terminate the sandbox.
- The verified behavior is based on the experiment recorded in `experiments/`.

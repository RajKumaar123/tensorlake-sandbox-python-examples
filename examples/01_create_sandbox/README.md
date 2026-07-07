# Example 01: Create Sandbox

This example shows how to create a Tensorlake sandbox from Python, inspect the returned metadata, and clean up the temporary sandbox afterward.

## Overview

The first Tensorlake example focuses on the core lifecycle:

1. Load credentials.
2. Create a sandbox.
3. Read basic metadata.
4. Terminate the temporary sandbox.

## Objective

Create the first Tensorlake sandbox successfully and print a small summary of its details.

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
python examples/01_create_sandbox/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` prints the sandbox ID, name, and status.
3. The example terminates the sandbox at the end because it is temporary.

## Expected Output

The script prints a creation message and a sandbox summary similar to this:

```text
Creating Tensorlake sandbox...
Sandbox created successfully.
```

The exact sandbox ID and status depend on the live Tensorlake service.
In the verified run for this repository, `Sandbox Name` was `None`.

## Key Learnings

- Sandbox creation is straightforward.
- API key authentication is required.
- Sandbox status is exposed as `SandboxStatus.RUNNING` after creation.

## Common Pitfalls

- Missing `TENSORLAKE_API_KEY` in `.env`
- Forgetting to terminate a temporary sandbox
- Assuming the SDK always returns a sandbox name

## Best Practices

- Use the shared helper functions in `utils/common.py`.
- Keep temporary sandbox examples self-cleaning.
- Verify live output before writing documentation.

## Notes

- The example handles a missing API key with a clear error message.
- The SDK may expose sandbox status as either a property or a method, so the example supports both forms.
- The sandbox is intentionally terminated at the end because this example uses a temporary sandbox.

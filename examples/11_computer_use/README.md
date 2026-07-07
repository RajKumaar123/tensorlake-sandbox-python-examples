# Example 11: Computer Use

This example demonstrates Tensorlake's desktop connection primitive for computer-use workflows.

## Overview

This example walks through the desktop connection flow:

1. Load credentials.
2. Create a named sandbox.
3. Inspect the desktop connection parameters.
4. Document the verified computer-use primitive.
5. Clean up the sandbox.

## Objective

Demonstrate the Tensorlake desktop connection primitive used for computer-use workflows.

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
python examples/11_computer_use/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates a named sandbox.
2. `main.py` documents the desktop connection parameters Tensorlake exposes.
3. The example emphasizes the verified `connect_desktop()` primitive.
4. The sandbox is terminated in `finally`.

## Expected Output

The script should print the sandbox information and the desktop connection parameters.

## Key Learnings

- Tensorlake exposes `connect_desktop()` for desktop access.
- Computer-use workflows are built on top of this desktop connection primitive.
- The sandbox should still be cleaned up after documentation and verification.

## Common Pitfalls

- Assuming a browser-specific GUI automation helper exists
- Forgetting that the desktop connection requires a named sandbox for lifecycle features
- Leaving the sandbox open after capturing the connection details

## Best Practices

- Use a named sandbox for computer-use workflows.
- Treat desktop connection parameters as environment-specific details.
- Clean up the sandbox after verification.

## Notes

- This example documents the verified desktop connection primitive rather than opening a live interactive GUI session in the test environment.

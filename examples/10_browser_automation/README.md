# Example 10: Browser Automation

This example demonstrates the interactive session primitive used for browser-style automation workflows in Tensorlake.

## Overview

This example walks through the browser-automation setup flow:

1. Load credentials.
2. Create a named sandbox.
3. Create an interactive PTY session.
4. Print the session credentials.
5. Clean up the sandbox.

## Objective

Create the interactive session primitive that browser automation workflows can build on.

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
python examples/10_browser_automation/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates a named sandbox.
2. `main.py` creates a PTY session with `create_pty_session()`.
3. The example prints the session ID and token returned by the SDK.
4. The sandbox is terminated in `finally`.

## Expected Output

The script should show the sandbox creation and the PTY session credentials.

## Key Learnings

- Tensorlake exposes PTY sessions for interactive workflows.
- `create_pty_session()` returns a traced payload containing `session_id` and `token`.
- These primitives are the foundation for browser-style automation work.

## Common Pitfalls

- Assuming a browser-specific helper exists when the SDK exposes PTY/desktop primitives instead
- Forgetting to name the sandbox when interactive lifecycle features are involved
- Leaving the sandbox open after capturing the session credentials

## Best Practices

- Use a named sandbox for interactive workflows.
- Treat the session token as sensitive information.
- Clean up the sandbox after verification.

## Notes

- This example demonstrates the automation primitive rather than a full browser UI flow.
- The traced PTY session output includes a session ID and token.

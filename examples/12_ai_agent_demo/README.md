# Example 12: AI Agent Demo

This example demonstrates a lightweight AI-agent style workflow inside Tensorlake.

## Overview

This example walks through the agent-style flow:

1. Load credentials.
2. Create a named sandbox.
3. Create an interactive PTY session.
4. Run a simple agent-style action inside the sandbox.
5. Clean up the sandbox.

## Objective

Demonstrate a simple AI-agent style workflow using Tensorlake sandbox primitives.

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
python examples/12_ai_agent_demo/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates a named sandbox.
2. `main.py` creates a PTY session to represent the interactive agent primitive.
3. The example runs a simple agent-style action with `run()`.
4. The sandbox is terminated in `finally`.

## Expected Output

The script should show the PTY session credentials and the simple action output.

## Key Learnings

- PTY sessions provide the interactive primitive needed for agent-style workflows.
- Simple command execution can be combined with session setup to demonstrate agent flow.
- Cleanup still matters even for demo-style workflows.

## Common Pitfalls

- Assuming a full AI agent framework exists in the SDK
- Forgetting to name the sandbox when using interactive primitives
- Leaving the sandbox open after the demo finishes

## Best Practices

- Keep the agent demo simple and explain the workflow clearly.
- Use the shared helpers in `utils/common.py`.
- Clean up the sandbox after verification.

## Notes

- This example demonstrates a lightweight agent workflow using verified Tensorlake primitives rather than a separate external agent framework.

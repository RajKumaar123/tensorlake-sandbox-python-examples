# Example 07: Suspend and Resume

This example shows how to suspend and resume a Tensorlake sandbox while preserving state.

## Overview

This example demonstrates the lifecycle flow:

1. Load credentials.
2. Create a sandbox.
3. Create state in the filesystem.
4. Suspend the sandbox.
5. Resume the sandbox.
6. Verify that the state is still present.
7. Clean up the sandbox.

## Objective

Suspend and resume a Tensorlake sandbox and confirm that filesystem state survives the lifecycle transition.

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
python examples/07_suspend_resume/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` creates a small file inside the sandbox.
3. The sandbox is suspended and then resumed.
4. The file is read back to confirm the state survived.
5. The sandbox is terminated in `finally` after verification.

## Expected Output

The script should show the sandbox being suspended, resumed, and then the preserved file being read successfully.

## Key Learnings

- `suspend()` and `resume()` are direct lifecycle calls on the sandbox object.
- Filesystem state survives suspension and resume.
- Lifecycle examples should still clean up the sandbox after verification.

## Common Pitfalls

- Assuming suspension clears filesystem state
- Forgetting to resume before verifying preserved data
- Leaving a lifecycle sandbox running after the test completes

## Best Practices

- Verify state after resuming, not before.
- Use the shared helpers in `utils/common.py`.
- Clean up the sandbox once the lifecycle behavior is confirmed.

## Notes

- This example focuses on lifecycle behavior, but it still terminates the sandbox after verification to avoid quota buildup.

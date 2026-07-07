# Example 09: Parallel Sandboxes

This example demonstrates how to create multiple sandboxes from a source sandbox copy and run work in the cloned sandboxes.

## Overview

This example walks through the parallel sandbox flow:

1. Load credentials.
2. Create a named source sandbox.
3. Clone the sandbox into multiple copies.
4. Connect to the clones.
5. Run a small command in each clone.
6. Clean up all sandboxes.

## Objective

Create parallel Tensorlake sandboxes from a source sandbox copy and verify that each clone can run independent work.

## Prerequisites

- Python 3.12+
- `tensorlake`
- `python-dotenv`
- A valid `TENSORLAKE_API_KEY` in `.env`

## Notes

- The live Tensorlake project used for verification enforced a sandbox quota limit during copying.
- The example still documents the copy workflow and records the actual quota failure as part of the learning outcome.

## Project Structure

- `main.py`
- `output.txt`

## How to Run

```bash
python examples/09_parallel_sandboxes/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates a named source sandbox.
2. `main.py` calls `copy(times=2)` to create sandbox clones.
3. The example connects to each cloned sandbox and runs a small command when the quota allows.
4. Every sandbox created by the example is cleaned up in `finally`.

## Expected Output

The script should show the source sandbox and either a successful clone workflow or the live quota failure encountered during verification.

## Key Learnings

- `copy(times=...)` can create multiple sandbox instances from one source.
- Cloning may be blocked by the project sandbox quota.
- Every created sandbox should be terminated after the example completes.

## Common Pitfalls

- Assuming `copy()` returns a single sandbox object rather than clone metadata
- Forgetting to connect to each clone before running work
- Leaving clone sandboxes running after verification
- Assuming quota will allow multiple running sandboxes during testing

## Best Practices

- Name the source sandbox so lifecycle features remain available.
- Clean up each clone individually.
- Keep the clone workload simple so the cloning behavior is the focus.
- Document quota limitations when they appear during verification.

## Notes

- This example intentionally creates and cleans up multiple sandboxes to demonstrate parallel sandbox creation.
- Live verification hit the project quota limit before clones could be created.

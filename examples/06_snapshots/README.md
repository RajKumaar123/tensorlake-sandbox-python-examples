# Example 06: Snapshots

This example demonstrates how to create, list, fetch, and delete a Tensorlake snapshot.

## Overview

This example walks through the snapshot lifecycle:

1. Load credentials.
2. Create a sandbox.
3. Create a snapshot with `checkpoint()`.
4. List available snapshots.
5. Fetch snapshot metadata.
6. Delete the snapshot.
7. Terminate the sandbox after the snapshot workflow completes.

## Objective

Create a snapshot from a Tensorlake sandbox and inspect it.

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
python examples/06_snapshots/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` creates a snapshot with `checkpoint()`.
3. The example lists snapshots and fetches the created snapshot.
4. The snapshot is deleted at the end to avoid leaving extra state behind.
5. The sandbox is terminated after the snapshot workflow completes so the example does not keep a running sandbox open.

## Expected Output

The script should show snapshot creation, listing, retrieval, and deletion.

The sandbox is terminated after the snapshot workflow completes.

## Key Learnings

- `checkpoint()` returns snapshot metadata when the snapshot is created.
- `list_snapshots()` can be used to inspect existing snapshots.
- `get_snapshot()` and `delete_snapshot()` work with the snapshot ID.
- The sandbox can still be cleaned up after the snapshot is verified.

## Common Pitfalls

- Assuming `checkpoint()` always returns the same shape in every SDK version
- Leaving snapshots behind after the example finishes

## Best Practices

- Verify the snapshot ID before fetching or deleting it.
- Clean up snapshots when you are done inspecting them.
- Terminate the sandbox after the snapshot workflow completes.

## Notes

- This example terminates the sandbox after the snapshot behavior is demonstrated.
- The snapshot is deleted at the end, and the running sandbox is cleaned up afterward.

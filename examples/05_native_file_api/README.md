# Example 05: Native File API

This example demonstrates Tensorlake's native file methods for writing, reading, listing, and deleting files.

## Overview

This example shows the SDK file APIs in action:

1. Load credentials.
2. Create a temporary sandbox.
3. Write a file with `write_file`.
4. Read it back with `read_file`.
5. List `/tmp` with `list_directory`.
6. Delete the file with `delete_file`.
7. Clean up the sandbox.

## Objective

Use the sandbox file APIs directly instead of shell commands.

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
python examples/05_native_file_api/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` writes, reads, lists, and deletes files with the native SDK methods.
3. The example prints the traced results so the SDK behavior is visible.
4. The sandbox is terminated in `finally` because this is a temporary example.

## Expected Output

The script should show each native file API step completing successfully.

The sandbox is intentionally terminated at the end because this is a temporary example.

## Key Learnings

- Native file APIs can be used directly instead of shell commands.
- `write_file` and `delete_file` return `None` in their traced `.value`.
- `read_file` returns bytes and `list_directory` returns directory metadata.

## Common Pitfalls

- Assuming native file methods return shell-like stdout/stderr output
- Forgetting that traced SDK calls expose their payload on `.value`
- Leaving a temporary sandbox running after the example completes

## Best Practices

- Use the shared helpers in `utils/common.py`.
- Inspect the traced return values rather than guessing their shape.
- Clean up temporary sandboxes in `finally`.

## Notes

- This example uses the SDK file APIs directly.
- The code handles cleanup so the example does not consume an extra running sandbox.
- `write_file` and `delete_file` return `None`, while `read_file` returns bytes and `list_directory` returns directory metadata.

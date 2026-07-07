# Example 04: Install Packages

This example shows how to install a Python package inside a Tensorlake sandbox and verify the installation.

## Overview

This example demonstrates the package-installation workflow:

1. Load credentials.
2. Create a temporary sandbox.
3. Install `pandas`.
4. Verify the installed package version.
5. Clean up the sandbox.

## Objective

Install `pandas` and confirm that it can be imported successfully inside the sandbox.

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
python examples/04_install_packages/main.py
```

## Code Explanation

1. `utils/common.py` loads the API key and creates the sandbox.
2. `main.py` installs `pandas` using `pip`.
3. The example verifies that `pandas` can be imported and prints the version.
4. The sandbox is terminated in `finally` because this is a temporary example.

## Expected Output

The script should show pip installing `pandas`, then print the installed pandas version.

The sandbox is intentionally terminated at the end because this is a temporary example.

## Key Learnings

- The sandbox Python environment is externally managed.
- `pip install` may require `--break-system-packages`.
- The installed `pandas` version can be verified immediately after installation.

## Common Pitfalls

- Forgetting the `--break-system-packages` flag
- Assuming the default `pip install` path will work in the sandbox
- Leaving a temporary sandbox running after the example completes

## Best Practices

- Use the shared helpers in `utils/common.py`.
- Verify the package after installation instead of assuming success.
- Clean up temporary sandboxes in `finally`.

## Notes

- This example follows the shared cleanup rule to avoid quota buildup.
- The exact package version may vary depending on the available wheel and environment.
- The sandbox runtime may require `--break-system-packages` because the Python environment is externally managed.

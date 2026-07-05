"""
run_commands.py

1. Load API key from .env
2. Create a Tensorlake sandbox
3. Execute a command inside the sandbox
4. Print the output
"""

from dotenv import load_dotenv
import os
from tensorlake.sandbox import Sandbox

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

api_key = os.getenv("TENSORLAKE_API_KEY")

if not api_key:
    raise ValueError("TENSORLAKE_API_KEY not found in .env")

# ---------------------------------------------------
# Create sandbox
# ---------------------------------------------------
print("Creating sandbox...")

sandbox = Sandbox.create(api_key=api_key)

print(f"Sandbox ID : {sandbox.sandbox_id}")
print(f"Status     : {sandbox.status}")

# ---------------------------------------------------
# Execute command
# ---------------------------------------------------
print("\nExecuting command...")

result = sandbox.run(
    command="python",
    args=["--version"]
)

# ---------------------------------------------------
# Print results
# ---------------------------------------------------
print("\nTrace ID:")
print(result.trace_id)

print("\nExit Code:")
print(result.exit_code)

print("\nSTDOUT:")
print(result.stdout)

print("\nSTDERR:")
print(result.stderr)
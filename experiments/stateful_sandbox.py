"""
stateful_sandbox.py

Demonstrate filesystem persistence in Tensorlake sandboxes
"""

from dotenv import load_dotenv
import os
from tensorlake.sandbox import Sandbox

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("TENSORLAKE_API_KEY")

# Create sandbox
print("Creating sandbox...")
sandbox = Sandbox.create(api_key=api_key)

print("Sandbox ID :", sandbox.sandbox_id)
print("Status     :", sandbox.status)

# -----------------------------------------------------
# Create a file
# -----------------------------------------------------
print("\nCreating file...")

result = sandbox.run(
    command="sh",
    args=["-c", "echo 'Hello Tensorlake!' > /tmp/hello.txt"]
)

print("Exit Code :", result.exit_code)
print("STDOUT    :", repr(result.stdout))
print("STDERR    :", repr(result.stderr))

# -----------------------------------------------------
# Read file
# -----------------------------------------------------
print("\nReading file...")

result = sandbox.run(
    command="cat",
    args=["/tmp/hello.txt"]
)

print("Exit Code :", result.exit_code)
print("STDOUT    :", repr(result.stdout))
print("STDERR    :", repr(result.stderr))

# -----------------------------------------------------
# List directory
# -----------------------------------------------------
print("\nListing /tmp...")

result = sandbox.run(
    command="ls",
    args=["-l", "/tmp"]
)

print(result.stdout)
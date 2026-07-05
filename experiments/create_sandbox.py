"""
create_sandbox.py

This script:
1. Loads the Tensorlake API key from the .env file.
2. Creates a new Tensorlake sandbox.
3. Displays sandbox information.
"""

# Load environment variables from .env
from dotenv import load_dotenv
import os

# Import Tensorlake Sandbox SDK
from tensorlake.sandbox import Sandbox

# --------------------------------------------------
# Step 1: Load variables from .env
# --------------------------------------------------
load_dotenv()

# Read the API key from .env
api_key = os.getenv("TENSORLAKE_API_KEY")

# Verify API key exists
if not api_key:
    raise ValueError(
        "TENSORLAKE_API_KEY not found. Please check your .env file."
    )

# --------------------------------------------------
# Step 2: Create a sandbox
# --------------------------------------------------
print("Creating Tensorlake sandbox...")

sandbox = Sandbox.create(
    api_key=api_key
)

print("Sandbox created successfully!")

# --------------------------------------------------
# Step 3: Display sandbox information
# --------------------------------------------------
print("\nSandbox Details")
print("-" * 50)

# Sandbox ID
print("Sandbox ID :", sandbox.sandbox_id)

# Sandbox Name
print("Sandbox Name :", sandbox.name)

# Sandbox Status
# Some SDK versions expose status as a property,
# others as a method, so we handle both.
try:
    status = sandbox.status()
except TypeError:
    status = sandbox.status

print("Sandbox Status :", status)

print("-" * 50)
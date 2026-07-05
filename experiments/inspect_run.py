from dotenv import load_dotenv
import os
from tensorlake.sandbox import Sandbox

load_dotenv()

api_key = os.getenv("TENSORLAKE_API_KEY")

print("Creating sandbox...")
sandbox = Sandbox.create(api_key=api_key)

print(f"Sandbox ID: {sandbox.sandbox_id}")
print(f"Status: {sandbox.status}")

print("\nRunning python --version")

result = sandbox.run(
    command="python",
    args=["--version"]
)

print("\nResult:")
print(result)
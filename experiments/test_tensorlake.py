from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

api_key = os.getenv("TENSORLAKE_API_KEY")

print("API Key loaded:", api_key[:15] + "..." if api_key else "Not found")

import tensorlake
print(dir(tensorlake))
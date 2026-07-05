from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("TENSORLAKE_API_KEY"))
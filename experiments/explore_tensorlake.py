import tensorlake

print("Cloud client:")
print(tensorlake.cloud_client)

print("\nAvailable methods:")
print(dir(tensorlake.cloud_client))

from dotenv import load_dotenv
import tensorlake

load_dotenv()


import inspect
from tensorlake.cloud_client import CloudClient

print(inspect.signature(CloudClient))

import inspect
from tensorlake.cloud_client import CloudClient

print(inspect.getsource(CloudClient))
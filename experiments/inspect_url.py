import inspect
import tensorlake.cloud_client as cc

print("USER_AGENT =", cc.USER_AGENT)

# Search for URL strings in the module source
source = inspect.getsource(cc)

for line in source.splitlines():
    if "http" in line.lower() or "url" in line.lower():
        print(line)
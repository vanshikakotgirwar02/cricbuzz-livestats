
from api.cricbuzz_client import get_live_matches

print("Testing Cricbuzz API...")

data = get_live_matches()

if data is None:
    print("API request failed. Check your API key, host, and endpoint.")
else:
    print("API connected successfully!")
    print(data)

import pandas as pd
import requests

def fetch_driver_position(meeting_key: int, session_key: int):
    url = f"https://api.openf1.org/v1/position?meeting_key={meeting_key}&session_key={session_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        pos = pd.DataFrame(response.json())
        print("Successfully fetched data")
        return pos
    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")
        return pd.DataFrame()
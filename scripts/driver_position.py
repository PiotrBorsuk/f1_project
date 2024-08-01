import pandas as pd
import requests
from datetime import datetime

def fetch_meetings_data():
    url = "https://api.openf1.org/v1/stints?session_key=9165"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        meetings_df = pd.DataFrame(response.json())
        meetings_df['date_start'] = pd.to_datetime(meetings_df['date_start'])
        print("Successfully fetched data")
        return meetings_df
    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")
        return pd.DataFrame()
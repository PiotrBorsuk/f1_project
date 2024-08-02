import pandas as pd
import requests
from datetime import datetime

def fetch_session_data(year: int, country: str):
    url = f"https://api.openf1.org/v1/sessions?country_name={country}&year={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        df = pd.DataFrame(response.json())
        df = df[['meeting_key','session_key','session_name']]
        session_key = df[df['session_name'] == 'Race'].session_key.iloc[0]
        meeting_key = df[df['session_name'] == 'Race'].meeting_key.iloc[0]
        print("Successfully fetched data")
        return meeting_key, session_key
    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")
        return pd.DataFrame()
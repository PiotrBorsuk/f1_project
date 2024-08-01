import pandas as pd
import requests
from datetime import datetime

def fetch_session_data(year: int, country: str):
    url = f"https://api.openf1.org/v1/sessions?country_name={country}&year={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        df = pd.DataFrame(response.json())
        df = df[['session_key','session_name']]
        print("Successfully fetched data")
        return df
    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")
        return pd.DataFrame()
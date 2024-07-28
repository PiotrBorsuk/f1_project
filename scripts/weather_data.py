import requests
import pandas as pd
from scripts.meetings_data import fetch_meetings_data

def fetch_weather_data(meeting_key: int):
    url = f"https://api.openf1.org/v1/weather?meeting_key={meeting_key}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_df = pd.DataFrame(response.json())
        weather_df['date'] = pd.to_datetime(weather_df['date'])
        meeting_df = fetch_meetings_data(meeting_key)
        df = pd.merge(weather_df, meeting_df, on='meeting_key')
        print("Successfully fetched data")
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
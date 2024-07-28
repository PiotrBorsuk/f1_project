import pandas as pd
import requests
from datetime import datetime

def fetch_meetings_data():
    url = "https://api.openf1.org/v1/meetings"

    response = requests.get(url)

    if response.status_code == 200:
        meetings_df = pd.DataFrame(response.json())
        meetings_df['date_start'] = pd.to_datetime(meetings_df['date_start'])
        print("Successfully fetched data")
        return meetings_df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
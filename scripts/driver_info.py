import pandas as pd
import requests

def fetch_driver_info(session_key: int):
    url = f"https://api.openf1.org/v1/drivers?&session_key={session_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        driver_info = pd.DataFrame(response.json())
        driver_info = driver_info[['driver_number','name_acronym','team_colour']]
        print("Successfully fetched data")
        return driver_info
    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")
        return pd.DataFrame()
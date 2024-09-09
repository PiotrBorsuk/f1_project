import pandas as pd
import requests
from datetime import datetime

class F1DataFetcher:

    BASE_URL = "https://api.openf1.org/v1"

    @staticmethod
    def _make_request(endpoint, params=None):
        url = f"{F1DataFetcher.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.RequestException as e:
            print(f"Failed to fetch data from {endpoint}. Error: {e}")
            return pd.DataFrame()

    @classmethod
    def fetch_session_info(cls, country: str, year: int):
        df = cls._make_request("sessions", params={"country_name":country, "year":year})
        return df

    @classmethod
    def fetch_meetings_data(cls):
        df = cls._make_request("meetings")
        if not df.empty:
            df['date_start'] = pd.to_datetime(df['date_start'])
        return df

    @classmethod
    def fetch_weather_data(cls, meeting_key: int):
        weather_df = cls._make_request("weather", params={"meeting_key": meeting_key})
        if not weather_df.empty:
            weather_df['date'] = pd.to_datetime(weather_df['date'])
            meeting_df = cls.fetch_meetings_data()
            df = pd.merge(weather_df, meeting_df, on='meeting_key')
            return df
        return pd.DataFrame()

    @classmethod
    def fetch_driver_position(cls, meeting_key: int, session_key: int):
        return cls._make_request("position", params={"meeting_key": meeting_key, "session_key": session_key})

    @classmethod
    def fetch_driver_info(cls, session_key: int):
        df = cls._make_request("drivers", params={"session_key": session_key})
        if not df.empty:
            return df[['driver_number', 'name_acronym', 'team_colour']]
        return df

    @classmethod
    def fetch_car_data(cls, session_key: int, driver_number: int):
        df = cls._make_request("car_data",
                               params={"session_key": session_key, "driver_number": driver_number}
                               )
        return df

    @classmethod
    def fetch_lap_info(cls, session_key: int, driver_number: int):
        df = cls._make_request("laps",
                               params={"session_key": session_key, "driver_number": driver_number}
                              )
        return df
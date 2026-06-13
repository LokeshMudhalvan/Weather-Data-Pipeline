import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def extract_weather_data():
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": [52.52, 12.23],
        "longitude": [13.41, 22.3],
        "hourly": "temperature_2m",
        "models": "jma_seamless",
    }
    responses = openmeteo.weather_api(url, params=params)
    temperature_df = pd.DataFrame()

    for response in responses:
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            )
        }

        hourly_data["temperatureInCelcius"] = hourly_temperature_2m
        hourly_df = pd.DataFrame(data=hourly_data)
        temperature_df = pd.concat([temperature_df, hourly_df], ignore_index=True)

    temperature_df.to_csv("weather.csv", sep="\t")
    print("\ntemperature data\n", temperature_df)
    return temperature_df

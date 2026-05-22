import pandas as pd
import os
import requests
from datetime import datetime


API_KEY = os.getenv("OPENWEATHER_API_KEY", "987ca7e951f6d62d8c482b40aa4acbf5")
def get_current_weather_DataFrame(cities_df):
    records=[]
    url = "https://api.openweathermap.org/data/2.5/weather"

    for _,row in cities_df.iterrows():
        try:
            params = {"lat": row["lat"], "lon": row["lang"], "appid": API_KEY, "units": "metric"}
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()
            data= r.json()
            record = {
                "global_cities_id":     row["global_id"],
                "table_cities_id":        row["id"],
                "dt":                   datetime.now(),
                "temp":         data["main"]["temp"],
                "feels_like":   data["main"]["feels_like"],
                "humidity":     data["main"]["humidity"],
                "weather_desc": data["weather"][0]["description"],
                "wind_speed":   data["wind"]["speed"],
                "visibility":   data.get("visibility"),
                "sunrise":      datetime.fromtimestamp(data["sys"]["sunrise"]),
                "sunset":       datetime.fromtimestamp(data["sys"]["sunset"]),
            }
            records.append(record)
        except Exception as e:
            print(f"Error {e}")

    #creating DataFrame:
    current_weather_df = pd.DataFrame(records)

    return current_weather_df


# =========================
# Forecast Weather Function
# =========================
def get_forecast_weather_DataFrame(cities_df):
    records = []
    # Loop through cities
    for _, row in cities_df.iterrows():

        try:
            # Forecast API endpoint
            url = "https://api.openweathermap.org/data/2.5/forecast"
            # API parameters
            params = {
                "lat": row["lat"],
                "lon": row["lang"],  
                "appid": API_KEY,
                "units": "metric"     # Celsius
            }

            # Request API
            response = requests.get(
                url,
                params=params,
                timeout=60
            )

            response.raise_for_status()
            data = response.json()
            # Forecast list
            forecasts = data["list"]
            # Loop through each forecast record
            for item in forecasts:

                record = {
                    "global_cities_id": row["global_id"],
                    "table_cities_id": row["id"],
                    "dt": datetime.fromtimestamp(item["dt"]),
                    "temp": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "humidity": item["main"]["humidity"],
                    "weather_desc": item["weather"][0]["description"],
                    "wind_speed": item["wind"]["speed"],
                    "sunrise": datetime.fromtimestamp(data["city"]["sunrise"]),
                    "sunset": datetime.fromtimestamp(data["city"]["sunset"])
                }

                records.append(record)
        except Exception as e:
            print(f"Error for city {row['id']} : {e}")

    # Create DataFrame
    forecast_weather_df = pd.DataFrame(records)

    return forecast_weather_df
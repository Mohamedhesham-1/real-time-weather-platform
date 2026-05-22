"""
DWH_load_layer.py

Purpose:
- Load fact_weather_observation
- Load fact_weather_forecast

Source schema:
    telbs_eh_final_proj

Target schema:
    telbs_eh_dwh

Important:
- Do NOT truncate fact_weather_observation.
- It is the historical weather table.
"""

from datetime import datetime
from OLTP_DB_connection import db_execute_conn


SOURCE_SCHEMA = "telbs_eh_final_proj"
DWH_SCHEMA = "telbs_eh_dwh"


def load_fact_weather_observation():
    """
    Load actual/current weather from OLTP_current_weather
    into DWH fact_weather_observation.

    Grain:
        One row per city per observation_datetime.

    Source:
        telbs_eh_final_proj.OLTP_current_weather

    Target:
        telbs_eh_dwh.fact_weather_observation
    """

    insert_sql = f"""
    INSERT INTO {DWH_SCHEMA}.fact_weather_observation (
        city_key,
        global_city_id,
        date_key,
        observation_datetime,
        temp,
        feels_like,
        humidity,
        wind_speed,
        visibility,
        weather_desc,
        sunrise,
        sunset,
        source_system
    )
    SELECT
        dc.city_key,
        cw.global_cities_id AS global_city_id,
        CAST(DATE_FORMAT(cw.dt, '%Y%m%d') AS UNSIGNED) AS date_key,
        cw.dt AS observation_datetime,
        cw.temp,
        cw.feels_like,
        cw.humidity,
        cw.wind_speed,
        cw.visibility,
        cw.weather_desc,
        cw.sunrise,
        cw.sunset,
        'OpenWeather_Current_API' AS source_system
    FROM {SOURCE_SCHEMA}.OLTP_current_weather cw
    INNER JOIN {DWH_SCHEMA}.dim_city dc
        ON cw.global_cities_id = dc.global_city_id
    INNER JOIN {DWH_SCHEMA}.dim_date dd
        ON CAST(DATE_FORMAT(cw.dt, '%Y%m%d') AS UNSIGNED) = dd.date_key
    WHERE cw.global_cities_id IS NOT NULL
      AND cw.dt IS NOT NULL
    ON DUPLICATE KEY UPDATE
        temp = VALUES(temp),
        feels_like = VALUES(feels_like),
        humidity = VALUES(humidity),
        wind_speed = VALUES(wind_speed),
        visibility = VALUES(visibility),
        weather_desc = VALUES(weather_desc),
        sunrise = VALUES(sunrise),
        sunset = VALUES(sunset),
        load_datetime = CURRENT_TIMESTAMP;
    """

    db_execute_conn(insert_sql)
    print("fact_weather_observation loaded successfully.")


def load_fact_weather_forecast():
    """
    Load forecast weather from OLTP_forcast_weather
    into DWH fact_weather_forecast.

    Grain:
        One row per city per forecast run per forecast_for_datetime.

    Source:
        telbs_eh_final_proj.OLTP_forcast_weather

    Target:
        telbs_eh_dwh.fact_weather_forecast
    """

    forecast_run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_sql = f"""
    INSERT INTO {DWH_SCHEMA}.fact_weather_forecast (
        city_key,
        global_city_id,
        forecast_date_key,
        forecast_run_datetime,
        forecast_for_datetime,
        temp,
        feels_like,
        humidity,
        wind_speed,
        weather_desc,
        sunrise,
        sunset,
        source_system
    )
    SELECT
        dc.city_key,
        fw.global_cities_id AS global_city_id,
        CAST(DATE_FORMAT(fw.dt, '%Y%m%d') AS UNSIGNED) AS forecast_date_key,
        '{forecast_run_datetime}' AS forecast_run_datetime,
        fw.dt AS forecast_for_datetime,
        fw.temp,
        fw.feels_like,
        fw.humidity,
        fw.wind_speed,
        fw.weather_desc,
        fw.sunrise,
        fw.sunset,
        'OpenWeather_Forecast_API' AS source_system
    FROM {SOURCE_SCHEMA}.OLTP_forcast_weather fw
    INNER JOIN {DWH_SCHEMA}.dim_city dc
        ON fw.global_cities_id = dc.global_city_id
    INNER JOIN {DWH_SCHEMA}.dim_date dd
        ON CAST(DATE_FORMAT(fw.dt, '%Y%m%d') AS UNSIGNED) = dd.date_key
    WHERE fw.global_cities_id IS NOT NULL
      AND fw.dt IS NOT NULL
    ON DUPLICATE KEY UPDATE
        temp = VALUES(temp),
        feels_like = VALUES(feels_like),
        humidity = VALUES(humidity),
        wind_speed = VALUES(wind_speed),
        weather_desc = VALUES(weather_desc),
        sunrise = VALUES(sunrise),
        sunset = VALUES(sunset),
        load_datetime = CURRENT_TIMESTAMP;
    """

    db_execute_conn(insert_sql)
    print("fact_weather_forecast loaded successfully.")


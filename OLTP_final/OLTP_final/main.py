import pandas as pd
from OLTP_DB_connection import db_query_conn , db_execute_conn , dataframe_to_sql_table
from API_wheather_gathering import get_current_weather_DataFrame , get_forecast_weather_DataFrame
from DWH.DWh_facts_loading import load_fact_weather_observation , load_fact_weather_forecast
from DWH.DWH_dim_date_loading import load_dim_date_from_current_weather , load_dim_date_from_forecast_weather

# Read all city latitude/longitude data from the OLTP gold view
City_lat_long_data=db_query_conn("select * from gold_city_state_lat_long")

# Call OpenWeather current weather API for all cities and return the result as a DataFrame
Current_wheather_for_cities=get_current_weather_DataFrame(City_lat_long_data)

# Append the latest current weather records into the DWH historical fact table
load_fact_weather_observation()

# Clear the OLTP current weather snapshot table before inserting the latest current weather data
db_execute_conn("truncate OLTP_current_weather")

# Insert the latest current weather DataFrame into the OLTP current weather table
dataframe_to_sql_table(Current_wheather_for_cities,"OLTP_current_weather")

# Insert/update date records in dim_date based on the new OLTP current weather data
load_dim_date_from_current_weather()

# Print success message after finishing the current weather pipeline
print("Current wheather done sucessfully")

# Call OpenWeather forecast API for all cities and return the result as a DataFrame
Forcast_wheather_for_cities=get_forecast_weather_DataFrame(City_lat_long_data)

# Append the latest forecast weather records into the DWH historical forecast fact table
load_fact_weather_forecast()

# Clear the OLTP forecast weather snapshot table before inserting the latest forecast weather data
db_execute_conn("truncate OLTP_forcast_weather")

# Insert the latest forecast weather DataFrame into the OLTP forecast weather table
dataframe_to_sql_table(Forcast_wheather_for_cities,"OLTP_forcast_weather")

# Insert/update date records in dim_date based on the new OLTP forecast weather data
load_dim_date_from_forecast_weather()

# Print success message after finishing the forecast weather pipeline
print("Forcast wheather done sucessfully")


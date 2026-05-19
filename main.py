import pandas as pd
from OLTP_DB_connection import get_db_connection , db_query_conn , db_execute_conn ,db_execute_many_conn , dataframe_to_sql_table
from API_wheather_gathering import get_current_weather_DataFrame , get_forecast_weather_DataFrame

City_lat_long_data=db_query_conn("select * from gold_city_state_lat_long")  # Task1
Current_wheather_for_cities=get_current_weather_DataFrame(City_lat_long_data)  #task2
db_execute_conn("truncate OLTP_current_weather") #Task3
dataframe_to_sql_table(Current_wheather_for_cities,"OLTP_current_weather") #task4
print("Current wheather done sucessfully")
Forcast_wheather_for_cities=get_forecast_weather_DataFrame(City_lat_long_data)  # task5
db_execute_conn("truncate OLTP_forcast_weather") #task6
dataframe_to_sql_table(Forcast_wheather_for_cities,"OLTP_forcast_weather") # task7
print("Forcast wheather done sucessfully")

## task8 : application that reads the current and forcast whaether to give insights to user (telbs eh)
## task9 : schedule forscast each 24 hrs -- schedule current each 2 hr

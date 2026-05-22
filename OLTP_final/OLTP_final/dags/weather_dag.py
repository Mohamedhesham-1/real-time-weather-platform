from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, '/opt/airflow/dags')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_current_weather():
    from OLTP_DB_connection import db_query_conn, db_execute_conn, dataframe_to_sql_table
    from API_wheather_gathering import get_current_weather_DataFrame
    from DWh_facts_loading import load_fact_weather_observation
    from DWH_dim_date_loading import load_dim_date_from_current_weather
    cities = db_query_conn("SELECT * FROM gold_city_state_lat_long")
    weather = get_current_weather_DataFrame(cities)
    load_fact_weather_observation()
    db_execute_conn("TRUNCATE TABLE OLTP_current_weather")
    dataframe_to_sql_table(weather, "OLTP_current_weather")
    load_dim_date_from_current_weather()

def run_forecast_weather():
    from OLTP_DB_connection import db_query_conn, db_execute_conn, dataframe_to_sql_table
    from API_wheather_gathering import get_forecast_weather_DataFrame
    from DWh_facts_loading import load_fact_weather_forecast
    from DWH_dim_date_loading import load_dim_date_from_forecast_weather
    cities = db_query_conn("SELECT * FROM gold_city_state_lat_long")
    forecast = get_forecast_weather_DataFrame(cities)
    load_fact_weather_forecast()
    db_execute_conn("TRUNCATE TABLE OLTP_forcast_weather")
    dataframe_to_sql_table(forecast, "OLTP_forcast_weather")
    load_dim_date_from_forecast_weather()

with DAG(
    dag_id='current_weather_dag',
    default_args=default_args,
    schedule='0 */2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'oltp', 'dwh'],
) as dag1:
    PythonOperator(
        task_id='fetch_and_load_current_weather',
        python_callable=run_current_weather,
    )

with DAG(
    dag_id='forecast_weather_dag',
    default_args=default_args,
    schedule='0 0 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'oltp', 'dwh'],
) as dag2:
    PythonOperator(
        task_id='fetch_and_load_forecast_weather',
        python_callable=run_forecast_weather,
    )

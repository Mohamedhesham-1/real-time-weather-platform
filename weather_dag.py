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

    cities = db_query_conn("select * from gold_city_state_lat_long")
    weather = get_current_weather_DataFrame(cities)
    db_execute_conn("truncate OLTP_current_weather")
    dataframe_to_sql_table(weather, "OLTP_current_weather")

def run_forecast_weather():
    from OLTP_DB_connection import db_query_conn, db_execute_conn, dataframe_to_sql_table
    from API_wheather_gathering import get_forecast_weather_DataFrame

    cities = db_query_conn("select * from gold_city_state_lat_long")
    forecast = get_forecast_weather_DataFrame(cities)
    db_execute_conn("truncate OLTP_forcast_weather")
    dataframe_to_sql_table(forecast, "OLTP_forcast_weather")

with DAG(
    dag_id='current_weather_dag',
    default_args=default_args,
    description='Fetch current weather every 2 hours',
    schedule='0 */2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag1:
    PythonOperator(
        task_id='fetch_current_weather',
        python_callable=run_current_weather,
    )

with DAG(
    dag_id='forecast_weather_dag',
    default_args=default_args,
    description='Fetch forecast weather every 24 hours',
    schedule='0 0 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag2:
    PythonOperator(
        task_id='fetch_forecast_weather',
        python_callable=run_forecast_weather,
    )
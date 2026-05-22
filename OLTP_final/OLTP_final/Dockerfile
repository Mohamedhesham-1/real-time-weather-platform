FROM apache/airflow:3.2.1-python3.11
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY API_wheather_gathering.py /opt/airflow/dags/
COPY OLTP_DB_connection.py /opt/airflow/dags/
COPY weather_dag.py /opt/airflow/dags/
COPY DWh_facts_loading.py /opt/airflow/dags/
COPY DWH_dim_date_loading.py /opt/airflow/dags/
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

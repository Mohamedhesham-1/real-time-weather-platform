"""
OLTP_DB_connection.py

Central MySQL connection helpers for the Telbs EH Final Project database.

Notes:
- db_query_conn(query) is for SELECT queries and returns a pandas DataFrame.
- db_execute_conn(query) is for DDL/DML statements like CREATE, DROP, ALTER, INSERT, UPDATE, DELETE.
"""

import mysql.connector
import pandas as pd
import numpy as np

# Database and schema and schema connection configuration

DB_NAME = "telbs_eh_final_proj"
DB_CONFIG = {
    "host": "172.24.160.1",
    "user": "root",
    "password": "Moh@med276@",
    "database": DB_NAME,
}


# connect to telbs eh schema
def get_db_connection():
    """Return a MySQL connection connected to the project database."""
    return mysql.connector.connect(**DB_CONFIG)

# Run DML and DQL and return data from database in daatframe form
def db_query_conn(query):
    """
    Run SELECT queries and return the result as a pandas DataFrame.

    Example:
        df = db_query_conn("SELECT * FROM gold_city_state_country")
    """
    conn = get_db_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# Run DDL Command on our OLTP Database
def db_execute_conn(query):
    """
    Run one non-SELECT SQL statement.

    Use this for:
    - CREATE DATABASE
    - CREATE TABLE
    - DROP TABLE
    - ALTER TABLE
    - INSERT / UPDATE / DELETE

    Args:
        query (str): SQL statement to execute.
        use_database (bool):
            True  -> connect to telbs_eh_final_proj database.
            False -> connect to MySQL server only, useful before database exists.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def db_execute_many_conn(query, values):
    """
    Run bulk INSERT using executemany.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(query, values)

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def dataframe_to_sql_table(df, table_name):
    """
    Insert pandas DataFrame rows into an existing SQL table.

    Notes:
    - DataFrame column names must match SQL table column names.
    - NaN values are converted to None.
    """

    # Replace NaN / NaT with None
    df = df.replace({np.nan: None})

    columns = list(df.columns)

    columns_sql = ", ".join([f"`{col}`" for col in columns])
    placeholders = ", ".join(["%s"] * len(columns))

    insert_query = f"""
        INSERT INTO `{table_name}` ({columns_sql})
        VALUES ({placeholders})
    """
    values = [tuple(row) for row in df.to_numpy()]

    db_execute_many_conn(insert_query, values)
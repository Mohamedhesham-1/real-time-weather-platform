"""
DWH_dim_date_loading.py

Purpose:
- Load/update dim_date in telbs_eh_dwh.
- Dates are extracted from OLTP_current_weather and OLTP_forcast_weather.
- This uses SQL statements executed through OLTP_DB_connection helper.

Run from project root:
    python DWH/DWH_dim_date_loading.py
"""

# Make project root importable
from OLTP_DB_connection import db_execute_conn


SOURCE_SCHEMA = "telbs_eh_final_proj"
DWH_SCHEMA = "telbs_eh_dwh"


def load_dim_date_from_current_weather():
    """
    Insert/update dim_date using dates from OLTP_current_weather.
    """

    sql = f"""
    INSERT INTO {DWH_SCHEMA}.dim_date (
        date_key,
        full_date,
        `day`,
        `month`,
        month_name,
        `quarter`,
        `year`,
        day_name,
        is_weekend
    )
    SELECT DISTINCT
        CAST(DATE_FORMAT(dt, '%Y%m%d') AS UNSIGNED) AS date_key,
        DATE(dt) AS full_date,
        DAY(dt) AS `day`,
        MONTH(dt) AS `month`,
        MONTHNAME(dt) AS month_name,
        QUARTER(dt) AS `quarter`,
        YEAR(dt) AS `year`,
        DAYNAME(dt) AS day_name,
        CASE
            WHEN DAYOFWEEK(dt) IN (1, 7) THEN TRUE
            ELSE FALSE
        END AS is_weekend
    FROM {SOURCE_SCHEMA}.OLTP_current_weather
    WHERE dt IS NOT NULL
    ON DUPLICATE KEY UPDATE
        full_date = VALUES(full_date),
        `day` = VALUES(`day`),
        `month` = VALUES(`month`),
        month_name = VALUES(month_name),
        `quarter` = VALUES(`quarter`),
        `year` = VALUES(`year`),
        day_name = VALUES(day_name),
        is_weekend = VALUES(is_weekend);
    """

    db_execute_conn(sql)
    print("dim_date loaded from OLTP_current_weather successfully.")


def load_dim_date_from_forecast_weather():
    """
    Insert/update dim_date using dates from OLTP_forcast_weather.
    """

    sql = f"""
    INSERT INTO {DWH_SCHEMA}.dim_date (
        date_key,
        full_date,
        `day`,
        `month`,
        month_name,
        `quarter`,
        `year`,
        day_name,
        is_weekend
    )
    SELECT DISTINCT
        CAST(DATE_FORMAT(dt, '%Y%m%d') AS UNSIGNED) AS date_key,
        DATE(dt) AS full_date,
        DAY(dt) AS `day`,
        MONTH(dt) AS `month`,
        MONTHNAME(dt) AS month_name,
        QUARTER(dt) AS `quarter`,
        YEAR(dt) AS `year`,
        DAYNAME(dt) AS day_name,
        CASE
            WHEN DAYOFWEEK(dt) IN (1, 7) THEN TRUE
            ELSE FALSE
        END AS is_weekend
    FROM {SOURCE_SCHEMA}.OLTP_forcast_weather
    WHERE dt IS NOT NULL
    ON DUPLICATE KEY UPDATE
        full_date = VALUES(full_date),
        `day` = VALUES(`day`),
        `month` = VALUES(`month`),
        month_name = VALUES(month_name),
        `quarter` = VALUES(`quarter`),
        `year` = VALUES(`year`),
        day_name = VALUES(day_name),
        is_weekend = VALUES(is_weekend);
    """

    db_execute_conn(sql)
    print("dim_date loaded from OLTP_forcast_weather successfully.")

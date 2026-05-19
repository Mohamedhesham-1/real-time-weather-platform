"""
DDL_layer.py

Purpose:
- Create the DDL layer for the Telbs EH Final Project database.
- This script creates the project database if it does not exist.
- Then it creates the Silver and Gold layer tables.
- It does NOT insert any data.

How to run:
    python DDL_layer.py

Important:
- DROP_EXISTING_TABLES = True will drop existing tables before recreating them.
- If you already have data and you do not want to delete it, set DROP_EXISTING_TABLES = False.

Required file in the same folder:
    OLTP_DB_connection.py
"""
import mysql.connector
from OLTP_DB_connection import DB_CONFIG, DB_NAME, db_execute_conn

# True  = drop existing tables and recreate them.
# False = try to create tables without dropping existing tables first.
DROP_EXISTING_TABLES = False


CREATE_DATABASE_DDL = f"""
CREATE DATABASE IF NOT EXISTS `{DB_NAME}`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_0900_ai_ci
"""

DROP_TABLES_DDL = [
    "SET FOREIGN_KEY_CHECKS = 0",
    "DROP TABLE IF EXISTS `gold_city_state_country`",
    "DROP TABLE IF EXISTS `silver_manual_geo_data`",
    "DROP TABLE IF EXISTS `silver_diffrent_string_same_state`",
    "DROP TABLE IF EXISTS `silver_cities_lat_long_not_found`",
    "DROP TABLE IF EXISTS `silver_cities_lat_long_mismatch`",
    "DROP TABLE IF EXISTS `silver_cities_lat_long`",
    "DROP VIEW IF EXISTS `gold_city_state_lat_long`",
    "SET FOREIGN_KEY_CHECKS = 1",
]


CREATE_TABLES_DDL = [
    """
    CREATE TABLE `silver_cities_lat_long` (
        `id` VARCHAR(20) NOT NULL,
        `city_name` VARCHAR(100) NOT NULL,
        `state_name` VARCHAR(100) DEFAULT NULL,
        `given_state_name` VARCHAR(100) NOT NULL,
        `country_code` VARCHAR(100) DEFAULT NULL,
        `lat` DECIMAL(10,8) DEFAULT NULL,
        `lang` DECIMAL(11,8) DEFAULT NULL,
        `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE `silver_cities_lat_long_mismatch` (
        `id` VARCHAR(20) NOT NULL,
        `city_name` VARCHAR(100) NOT NULL,
        `state_name` VARCHAR(100) NOT NULL,
        `given_state_name` VARCHAR(100) NOT NULL,
        `country_code` VARCHAR(100) DEFAULT NULL,
        `lat` DECIMAL(10,8) DEFAULT NULL,
        `lang` DECIMAL(11,8) DEFAULT NULL,
        `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE `silver_cities_lat_long_not_found` (
        `id` VARCHAR(20) NOT NULL,
        `city_name` VARCHAR(100) NOT NULL,
        `state_name` VARCHAR(100) NOT NULL,
        `given_state_name` VARCHAR(100) NOT NULL,
        `country_code` VARCHAR(100) DEFAULT NULL,
        `lat` DECIMAL(10,8) DEFAULT NULL,
        `lang` DECIMAL(11,8) DEFAULT NULL,
        `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE `silver_diffrent_string_same_state` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `CSV_state` VARCHAR(100) NOT NULL,
        `API_state` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE `silver_manual_geo_data` (
        `id` VARCHAR(20) NOT NULL,
        `city_name` VARCHAR(100) NOT NULL,
        `state_name` VARCHAR(100) NOT NULL,
        `given_state_name` VARCHAR(100) NOT NULL,
        `country_code` VARCHAR(100) DEFAULT NULL,
        `lat` DECIMAL(10,8) DEFAULT NULL,
        `lang` DECIMAL(11,8) DEFAULT NULL,
        `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE `gold_city_state_country` (
        `global_id` INT NOT NULL AUTO_INCREMENT,
        `city_name` VARCHAR(150) NOT NULL,
        `state_name` VARCHAR(150) NOT NULL,
        `country_code` VARCHAR(50) NOT NULL,
        PRIMARY KEY (`global_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    create view gold_city_state_lat_long AS
    select b.global_id , a.*  from (
    select * from silver_cities_lat_long 
    union
    select * from silver_manual_geo_data) a
    left join gold_city_state_country b
    on a.city_name = b.city_name
    """
        ,
    """
    CREATE TABLE `OLTP_current_weather` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `global_cities_id` INT DEFAULT NULL,
        `table_cities_id` varchar(20) NOT NULL,
        `dt` DATETIME DEFAULT NULL,
        `temp` FLOAT DEFAULT NULL,
        `feels_like` FLOAT DEFAULT NULL,
        `humidity` INT DEFAULT NULL,
        `weather_desc` VARCHAR(100) DEFAULT NULL,
        `wind_speed` FLOAT DEFAULT NULL,
        `visibility` INT DEFAULT NULL,
        `sunrise` DATETIME DEFAULT NULL,
        `sunset` DATETIME DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """,
    """
    CREATE TABLE OLTP_forcast_weather (
            `id` INT NOT NULL AUTO_INCREMENT,
            `global_cities_id` INT DEFAULT NULL,
            `table_cities_id` varchar(20) NOT NULL,
            `dt` DATETIME DEFAULT NULL,
            `temp` FLOAT DEFAULT NULL,
            `feels_like` FLOAT DEFAULT NULL,
            `humidity` INT DEFAULT NULL,
            `weather_desc` VARCHAR(100) DEFAULT NULL,
            `wind_speed` FLOAT DEFAULT NULL,
            `sunrise` DATETIME DEFAULT NULL,
            `sunset` DATETIME DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """
]


# Indexes only.
# These do not change columns, data types, or table structure.
# They only improve search/join/filter performance.
CREATE_INDEXES_DDL = [
    # silver_cities_lat_long
    "CREATE INDEX `idx_scl_city_given_country` ON `silver_cities_lat_long` (`city_name`, `given_state_name`, `country_code`)",
    "CREATE INDEX `idx_scl_state_name` ON `silver_cities_lat_long` (`state_name`)",
    "CREATE INDEX `idx_scl_country_code` ON `silver_cities_lat_long` (`country_code`)",

    # silver_cities_lat_long_mismatch
    "CREATE INDEX `idx_sclm_city_given_country` ON `silver_cities_lat_long_mismatch` (`city_name`, `given_state_name`, `country_code`)",
    "CREATE INDEX `idx_sclm_state_name` ON `silver_cities_lat_long_mismatch` (`state_name`)",
    "CREATE INDEX `idx_sclm_country_code` ON `silver_cities_lat_long_mismatch` (`country_code`)",

    # silver_cities_lat_long_not_found
    "CREATE INDEX `idx_sclnf_city_given_country` ON `silver_cities_lat_long_not_found` (`city_name`, `given_state_name`, `country_code`)",
    "CREATE INDEX `idx_sclnf_state_name` ON `silver_cities_lat_long_not_found` (`state_name`)",
    "CREATE INDEX `idx_sclnf_country_code` ON `silver_cities_lat_long_not_found` (`country_code`)",

    # silver_manual_geo_data
    "CREATE INDEX `idx_smgd_city_given_country` ON `silver_manual_geo_data` (`city_name`, `given_state_name`, `country_code`)",
    "CREATE INDEX `idx_smgd_state_name` ON `silver_manual_geo_data` (`state_name`)",
    "CREATE INDEX `idx_smgd_country_code` ON `silver_manual_geo_data` (`country_code`)",

    # silver_diffrent_string_same_state
    "CREATE INDEX `idx_sdsss_csv_api_state` ON `silver_diffrent_string_same_state` (`CSV_state`, `API_state`)",
    "CREATE INDEX `idx_sdsss_api_state` ON `silver_diffrent_string_same_state` (`API_state`)",

    # gold_city_state_country
    "CREATE INDEX `idx_gold_city_state_country` ON `gold_city_state_country` (`city_name`, `state_name`, `country_code`)",
    "CREATE INDEX `idx_gold_country_code` ON `gold_city_state_country` (`country_code`)",

    # OLTP_current_weather
    "CREATE INDEX `idx_weather_cities_id` ON `OLTP_current_weather` (`cities_id`)",
    "CREATE INDEX `idx_weather_dt` ON `OLTP_current_weather` (`dt`)",
    "CREATE INDEX `idx_weather_city_dt` ON `OLTP_current_weather` (`cities_id`, `dt`)",
]



def create_database_if_not_exists():
    """
    Create the database before using db_execute_conn().

    db_execute_conn() connects directly to DB_NAME.
    If the database does not exist yet, that connection will fail.
    So this function connects to MySQL server without selecting a database first.
    """
    server_config = DB_CONFIG.copy()
    server_config.pop("database", None)

    conn = mysql.connector.connect(**server_config)
    cursor = conn.cursor()

    try:
        cursor.execute(CREATE_DATABASE_DDL)
        conn.commit()
        print(f"Database `{DB_NAME}` is ready.")
    finally:
        cursor.close()
        conn.close()


def execute_statements(statements, step_name):
    """Execute SQL statements one by one using db_execute_conn()."""
    print(step_name)

    for statement in statements:
        sql = statement.strip()

        if not sql:
            continue

        db_execute_conn(sql)
        print(f"Executed: {sql.splitlines()[0][:100]}")


def execute_index_statements(statements):
    """
    Execute index creation statements.

    If DROP_EXISTING_TABLES = False and the index already exists,
    MySQL error 1061 is ignored so the script can continue.
    """
    print("Creating indexes only...")

    for statement in statements:
        sql = statement.strip()

        if not sql:
            continue

        try:
            db_execute_conn(sql)
            print(f"Created index: {sql.split('`')[1]}")
        except mysql.connector.Error as error:
            if error.errno == mysql.connector.errorcode.ER_DUP_KEYNAME:
                print(f"Skipped existing index: {sql.split('`')[1]}")
            else:
                raise


def create_ddl_layer():
    """Create the exact DDL layer from the provided tables, then add indexes only."""
    create_database_if_not_exists()

    if DROP_EXISTING_TABLES:
        execute_statements(DROP_TABLES_DDL, "Dropping existing tables...")
    else:
        print("Skipping table drop because DROP_EXISTING_TABLES = False.")

    execute_statements(CREATE_TABLES_DDL, "Creating exact Silver and Gold tables...")
    execute_index_statements(CREATE_INDEXES_DDL)

    print("DDL layer created successfully with indexes only added.")


if __name__ == "__main__":
    create_ddl_layer()

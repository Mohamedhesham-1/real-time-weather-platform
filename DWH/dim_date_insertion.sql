-- =====================================================
-- 2. Load missing dates from OLTP_current_weather
-- =====================================================

INSERT INTO telbs_eh_dwh.dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_name,
    is_weekend
)
SELECT DISTINCT
    CAST(DATE_FORMAT(dt, '%Y%m%d') AS UNSIGNED) AS date_key,
    DATE(dt) AS full_date,
    DAY(dt) AS day,
    MONTH(dt) AS month,
    MONTHNAME(dt) AS month_name,
    QUARTER(dt) AS quarter,
    YEAR(dt) AS year,
    DAYNAME(dt) AS day_name,
    CASE
        WHEN DAYOFWEEK(dt) IN (1, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM telbs_eh_final_proj.OLTP_current_weather
WHERE dt IS NOT NULL
ON DUPLICATE KEY UPDATE
    full_date = VALUES(full_date);
    
-- =====================================================
-- 3. Load missing dates from OLTP_forcast_weather
-- =====================================================

INSERT INTO telbs_eh_dwh.dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_name,
    is_weekend
)
SELECT DISTINCT
    CAST(DATE_FORMAT(dt, '%Y%m%d') AS UNSIGNED) AS date_key,
    DATE(dt) AS full_date,
    DAY(dt) AS day,
    MONTH(dt) AS month,
    MONTHNAME(dt) AS month_name,
    QUARTER(dt) AS quarter,
    YEAR(dt) AS year,
    DAYNAME(dt) AS day_name,
    CASE
        WHEN DAYOFWEEK(dt) IN (1, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM telbs_eh_final_proj.OLTP_forcast_weather
WHERE dt IS NOT NULL
ON DUPLICATE KEY UPDATE
    full_date = VALUES(full_date);
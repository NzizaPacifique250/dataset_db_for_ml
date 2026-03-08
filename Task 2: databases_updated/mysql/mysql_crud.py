import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DB = os.getenv("MYSQL_DB")

# -------------------------------
# Create MySQL connection
# -------------------------------
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# -------------------------------
# Read full traffic record
# -------------------------------
query_full = """
SELECT t.primary_id, t.traffic_volume, t.temp, t.rain_1h, t.snow_1h, t.clouds_all, t.lag_1, t.lag_24,
        t.lag_168, t.rolling_mean_24, t.rolling_mean_168,
        d.date_time, d.year, d.month, d.day, d.hour, d.day_of_week, d.is_weekend, 
        h.holiday, w.weather_main
FROM traffic t
JOIN datetime_info d ON t.datetime_id = d.datetime_id
JOIN holiday_info h ON t.holiday_id = h.holiday_id
JOIN weather_info w ON t.weather_id = w.weather_id;
"""

df_full = pd.read_sql(query_full, engine)
print("\nFull joined dataset preview:")
print(df_full.head())

# -------------------------------
# Select records by date range
# -------------------------------
query_range = """
SELECT *
FROM traffic t
JOIN datetime_info d ON t.datetime_id = d.datetime_id
WHERE d.date_time BETWEEN '2014-06-01' AND '2014-06-07';
"""

df_range = pd.read_sql(query_range, engine)
print("\nRecords from June 1 to June 7:")
print(df_range.head())


#-------------------------------------
# Query Individual column for prediction exact data with time
#-------------------------------------
query_range = """
SELECT *
FROM traffic t
JOIN datetime_info d ON t.datetime_id = d.datetime_id
WHERE d.date_time ='2014-06-01 04:00:00';
"""

df_range = pd.read_sql(query_range, engine)
print("\nRecords from June 1 to June 7:")
print(df_range.head())

# -------------------------------
# 3️⃣ Aggregate average traffic by hour
# # -------------------------------
query_hourly = """
SELECT d.hour, AVG(t.traffic_volume) AS avg_traffic
FROM traffic t
JOIN datetime_info d ON t.datetime_id = d.datetime_id
GROUP BY d.hour
ORDER BY d.hour;
"""

df_hourly = pd.read_sql(query_hourly, engine)
print("\nAverage traffic per hour:")
print(df_hourly)

# -------------------------------
# 4️⃣ Update a record
# -------------------------------
with engine.begin() as conn:
    conn.execute(
        text("UPDATE traffic SET traffic_volume = :value WHERE primary_id = :id"),
        {"value": 3418, "id": 1}
    )

print("\nRecord updated successfully.")

# -------------------------------
# 5️⃣ Delete a record
# -------------------------------
with engine.begin() as conn:
    conn.execute(
        text("DELETE FROM traffic WHERE primary_id = :id"),
        {"id": 2}
    )

print("Record deleted successfully.")
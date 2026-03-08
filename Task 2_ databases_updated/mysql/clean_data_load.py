import pandas as pd
from sqlalchemy import create_engine, text
import os
import kagglehub
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
# Load and clean data
# -------------------------------
path = kagglehub.dataset_download("mikedev/metro-traffic-volume")
csv_file = os.path.join(path, "Metro_Interstate_Traffic_Volume.csv")
df = pd.read_csv(csv_file)

# Fill missing holidays
df['holiday'] = df['holiday'].fillna('No')

# Convert datetime
df['date_time'] = pd.to_datetime(df['date_time'])

# Date/time features
df['day_of_week'] = df['date_time'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
df['year'] = df['date_time'].dt.year
df['month'] = df['date_time'].dt.month
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour

# Lag features
df['lag_1'] = df['traffic_volume'].shift(1)
df['lag_24'] = df['traffic_volume'].shift(24)
df['lag_168'] = df['traffic_volume'].shift(168)

# Rolling averages
df['rolling_mean_24'] = df['traffic_volume'].rolling(24).mean()
df['rolling_mean_168'] = df['traffic_volume'].rolling(168).mean()

# Drop rows with nulls from lag/rolling
df.dropna(inplace=True)

# Drop unnecessary columns if they exist
df.drop(columns=['weather_description'], inplace=True, errors='ignore')

# -------------------------------
# Create lookup tables
# -------------------------------
df_holiday = pd.DataFrame(df['holiday'].unique(), columns=['holiday'])
df_holiday['holiday_id'] = df_holiday.index + 1

df_weather = pd.DataFrame(df['weather_main'].unique(), columns=['weather_main'])
df_weather['weather_id'] = df_weather.index + 1

df_datetime = df[['date_time','year','month','day','hour', 'day_of_week', 'is_weekend']].copy()
df_datetime['datetime_id'] = df_datetime.index + 1

# Merge IDs into main traffic dataframe
df = df.merge(df_holiday, left_on='holiday', right_on='holiday', how='left')
df = df.merge(df_weather, left_on='weather_main', right_on='weather_main', how='left')
df = df.merge(df_datetime, left_on='date_time', right_on='date_time', how='left')

df_traffic = df[['temp','rain_1h','snow_1h','clouds_all','datetime_id','holiday_id','weather_id', 'traffic_volume', 'lag_1', 'lag_24', 'lag_168', 'rolling_mean_24', 'rolling_mean_168']].copy()
df_traffic['primary_id'] = df_traffic.index + 1
df_traffic = df_traffic[['primary_id','holiday_id', 'weather_id', 'datetime_id', 'temp','rain_1h','snow_1h','clouds_all','traffic_volume', 'lag_1', 'lag_24', 'lag_168', 'rolling_mean_24', 'rolling_mean_168']]

# -------------------------------
# Save to MySQL (Option A: truncate, then insert)
# -------------------------------
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

with engine.begin() as conn:
    # Disable FK checks to safely truncate tables
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    # Truncate tables instead of dropping
    conn.execute(text("TRUNCATE TABLE traffic;"))
    conn.execute(text("TRUNCATE TABLE holiday_info;"))
    conn.execute(text("TRUNCATE TABLE weather_info;"))
    conn.execute(text("TRUNCATE TABLE datetime_info;"))
    
    # Insert fresh data
    df_holiday.to_sql('holiday_info', conn, if_exists='append', index=False)
    df_weather.to_sql('weather_info', conn, if_exists='append', index=False)
    df_datetime.to_sql('datetime_info', conn, if_exists='append', index=False)
    df_traffic.to_sql('traffic', conn, if_exists='append', index=False)
    
    # Re-enable FK checks
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

print("✅ Data successfully loaded into MySQL using Option A (truncate + append)!")
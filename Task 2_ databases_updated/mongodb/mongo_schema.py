# mongo_schema.py
import pandas as pd
import os
import kagglehub
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # e.g. "mongodb://localhost:27017/"
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = "traffic_data"

# Load and clean data
path = kagglehub.dataset_download("mikedev/metro-traffic-volume")
csv_file = os.path.join(path, "Metro_Interstate_Traffic_Volume.csv")
df = pd.read_csv(csv_file)


df['holiday'] = df['holiday'].fillna('No')
df['date_time'] = pd.to_datetime(df['date_time'])
df['day_of_week'] = df['date_time'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)  # weekend: Sat(5)/Sun(6)
df['year'] = df['date_time'].dt.year
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour
# Lagging (shift) and moving averages (roll)
df['lag_1'] = df['traffic_volume'].shift(1)
df['lag_24'] = df['traffic_volume'].shift(24)
df['lag_168'] = df['traffic_volume'].shift(168)
df['rolling_mean_24'] = df['traffic_volume'].rolling(24).mean()
df['rolling_mean_168'] = df['traffic_volume'].rolling(168).mean()

# Drop rows with nulls created by lag/rolling
df.dropna(inplace=True)

# Drop unccessary columns
df.drop(columns=['weather_description'])

# -------------------------------
# Prepare documents for MongoDB
# -------------------------------
documents = []
for _, row in df.iterrows():
    doc = {
        "date_time": row['date_time'],
        "year": int(row['year']),
        "day": int(row['day']),
        "hour": int(row['hour']),
        "day_of_week": int(row['day_of_week']),
        "is_weekend": int(row['is_weekend']),
        "holiday": row['holiday'],
        "weather_main": row['weather_main'],
        "temp": float(row['temp']),
        "rain_1h": float(row['rain_1h']),
        "snow_1h": float(row['snow_1h']),
        "clouds_all": float(row['clouds_all']),
        "traffic_volume": int(row['traffic_volume']),
        "lag_1": float(row['lag_1']),
        "lag_24": float(row['lag_24']),
        "lag_168": float(row['lag_168']),
        "rolling_mean_24": float(row['rolling_mean_24']),
        "rolling_mean_168": float(row['rolling_mean_168'])
    }
    documents.append(doc)

# -------------------------------
# Connect to MongoDB and insert data
# -------------------------------
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Replace existing collection
collection.drop()
collection.insert_many(documents)

# Create index on date_time for faster queries in CRUD operations
collection.create_index("date_time")

print(f" {len(documents)} records inserted into MongoDB collection '{MONGO_COLLECTION}'")
print(f" Index on 'date_time' created for fast queries")
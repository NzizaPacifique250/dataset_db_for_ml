"""
Load MongoDB sample data from collection_design.js
This script populates the traffic_data collection with sample documents
"""
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['traffic_db']

# Drop existing collection and recreate
db.traffic_data.drop()

# Create collection with indexes
db.create_collection('traffic_data')
db.traffic_data.create_index([('date_time', 1)])
db.traffic_data.create_index([('weather.main', 1)])
db.traffic_data.create_index([('holiday', 1)])

# Insert sample documents
sample_docs = [
    {
        "date_time": datetime(2012, 10, 2, 9, 0, 0),
        "traffic_volume": 5545,
        "weather": {
            "main": "Clouds",
            "description": "scattered clouds",
            "temp": 288.28,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 40
        },
        "holiday": None
    },
    {
        "date_time": datetime(2012, 10, 2, 10, 0, 0),
        "traffic_volume": 4516,
        "weather": {
            "main": "Clouds",
            "description": "broken clouds",
            "temp": 289.36,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 75
        },
        "holiday": None
    },
    {
        "date_time": datetime(2012, 10, 2, 11, 0, 0),
        "traffic_volume": 4767,
        "weather": {
            "main": "Clouds",
            "description": "broken clouds",
            "temp": 289.58,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 75
        },
        "holiday": None
    },
    {
        "date_time": datetime(2012, 10, 2, 12, 0, 0),
        "traffic_volume": 5026,
        "weather": {
            "main": "Clear",
            "description": "sky is clear",
            "temp": 289.87,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 0
        },
        "holiday": None
    },
    {
        "date_time": datetime(2012, 10, 2, 13, 0, 0),
        "traffic_volume": 4918,
        "weather": {
            "main": "Clouds",
            "description": "few clouds",
            "temp": 291.28,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 20
        },
        "holiday": None
    },
    {
        "date_time": datetime(2016, 7, 4, 14, 0, 0),
        "traffic_volume": 2045,
        "weather": {
            "main": "Clear",
            "description": "sky is clear",
            "temp": 302.15,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 0
        },
        "holiday": "Independence Day"
    },
    {
        "date_time": datetime(2013, 12, 25, 8, 0, 0),
        "traffic_volume": 1134,
        "weather": {
            "main": "Snow",
            "description": "light snow",
            "temp": 261.48,
            "rain_1h": 0.0,
            "snow_1h": 0.5,
            "clouds_all": 90
        },
        "holiday": "Christmas Day"
    },
    {
        "date_time": datetime(2014, 9, 1, 8, 0, 0),
        "traffic_volume": 1876,
        "weather": {
            "main": "Clear",
            "description": "sky is clear",
            "temp": 291.48,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 0
        },
        "holiday": "Labor Day"
    },
    {
        "date_time": datetime(2018, 1, 15, 7, 0, 0),
        "traffic_volume": 1789,
        "weather": {
            "main": "Snow",
            "description": "snow",
            "temp": 258.93,
            "rain_1h": 0.0,
            "snow_1h": 1.2,
            "clouds_all": 90
        },
        "holiday": "Martin Luther King Jr Day"
    },
    {
        "date_time": datetime(2017, 11, 23, 16, 0, 0),
        "traffic_volume": 4321,
        "weather": {
            "main": "Rain",
            "description": "light rain",
            "temp": 279.15,
            "rain_1h": 0.25,
            "snow_1h": 0.0,
            "clouds_all": 90
        },
        "holiday": "Thanksgiving Day"
    }
]

result = db.traffic_data.insert_many(sample_docs)
print(f"✓ Successfully inserted {len(result.inserted_ids)} documents into MongoDB")
print(f"✓ Total documents in collection: {db.traffic_data.count_documents({})}")

# Verify collection
sample = db.traffic_data.find_one()
print(f"✓ Sample document: {sample['date_time']} - {sample['traffic_volume']} vehicles")

client.close()

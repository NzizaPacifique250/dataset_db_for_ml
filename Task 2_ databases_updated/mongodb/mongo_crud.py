# mongo_crud.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")  # e.g. "mongodb://localhost:27017/"
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = "traffic_data"

# -------------------------------
# Connect to MongoDB
# -------------------------------
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# -------------------------------
# CREATE: Insert a new record
# -------------------------------
def create_record(doc: dict):
    """Insert a single document into MongoDB"""
    result = collection.insert_one(doc)
    return result.inserted_id

# -------------------------------
# READ: Get the latest record
# -------------------------------
def get_latest_record():
    """Get the most recent record based on date_time"""
    return collection.find_one(sort=[("date_time", -1)])

# -------------------------------
# READ: Get a single record by datetime
# -------------------------------
def get_record_by_datetime(dt: datetime):
    """Get a single record matching a specific datetime"""
    return collection.find_one({"date_time": dt})

# -------------------------------
# READ: Get records in a date range
# -------------------------------
def get_records_by_date_range(start: datetime, end: datetime):
    """Get all records between start and end datetime"""
    return list(collection.find({"date_time": {"$gte": start, "$lte": end}}))

# -------------------------------
# READ: Get first N records
# -------------------------------
def get_first_n_records(n: int = 10):
    """Get the first n records in the collection"""
    return list(collection.find().limit(n))

# -------------------------------
# UPDATE: Update traffic_volume for a record
# -------------------------------
def update_traffic_volume(dt: datetime, new_volume: int):
    """Update the traffic_volume for a record with a specific datetime"""
    result = collection.update_one({"date_time": dt}, {"$set": {"traffic_volume": new_volume}})
    return result.modified_count

# -------------------------------
# DELETE: Remove a record by datetime
# -------------------------------
def delete_record_by_datetime(dt: datetime):
    """Delete a record with a specific datetime"""
    result = collection.delete_one({"date_time": dt})
    return result.deleted_count

# -------------------------------
# EXAMPLES
# -------------------------------
if __name__ == "__main__":
    print("---- Latest record ----")
    latest = get_latest_record()
    print(latest)

    print("\n---- First 10 records ----")
    first_10 = get_first_n_records(10)
    for rec in first_10:
        print(rec)

    # Example datetime to test single record retrieval
    example_dt = latest['date_time'] if latest else datetime(2018, 9, 3)
    print("\n---- Single record ----")
    single = get_record_by_datetime(example_dt)
    print(single)

    # Example date range
    start = datetime(2018, 9, 3)
    end = datetime(2018, 9, 4)
    print("\n---- Records in date range ----")
    range_records = get_records_by_date_range(start, end)
    for rec in range_records:
        print(rec)

    # Update example
    if latest:
        print("\n---- Updating latest record traffic_volume by +10 ----")
        modified = update_traffic_volume(latest['date_time'], latest['traffic_volume'] + 10)
        print(f"Modified {modified} record(s)")

    # Delete example (be careful!)
    if latest:
        print("\n---- Deleting latest record ----")
        deleted = delete_record_by_datetime(latest['date_time'])
        print(f"Deleted {deleted} record(s)")
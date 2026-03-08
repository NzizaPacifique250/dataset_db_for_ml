# mongodb_crud_api.py
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = "traffic_data"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

router = APIRouter(prefix="/mongo", tags=["MongoDB"])

# -------------------------------
# Pydantic model
# -------------------------------
class TrafficRecord(BaseModel):
    date_time: datetime
    traffic_volume: int
    rain_1h: float
    snow_1h: float
    clouds_all: int
    holiday: str
    weather_main: str
    lag_1: float = None
    lag_24: float = None
    lag_168: float = None
    rolling_mean_24: float = None
    rolling_mean_168: float = None

# -------------------------------
# GET latest record
# -------------------------------
@router.get("/latest")
def get_latest():
    record = collection.find_one(sort=[("date_time", -1)])
    if not record:
        raise HTTPException(status_code=404, detail="No records found")
    record["_id"] = str(record["_id"])
    return record

# -------------------------------
# GET record by datetime
# -------------------------------
@router.get("/single")
def get_single(date_time: datetime):
    record = collection.find_one({"date_time": date_time})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record["_id"] = str(record["_id"])
    return record

# -------------------------------
# GET last 24 records leading up to a given datetime
# -------------------------------
@router.get("/last24")
def get_last_24(date_time: datetime):
    """
    Returns the last 24 records leading up to the given datetime.
    Input is a datetime object, same as /single endpoint.
    """
    # Find last 24 records where date_time <= input
    records = list(
        collection.find({"date_time": {"$lte": date_time}})
                  .sort("date_time", -1)  # descending order (latest first)
                  .limit(24)
    )

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    # Convert MongoDB _id to string
    for r in records:
        r["_id"] = str(r["_id"])

    # Reverse to chronological order (oldest first)
    return list(records)


# -------------------------------
# GET records by date range
# -------------------------------
@router.get("/range")
def get_by_range(start: datetime, end: datetime):
    records = list(collection.find({"date_time": {"$gte": start, "$lte": end}}))
    for r in records:
        r["_id"] = str(r["_id"])
    return records

# -------------------------------
# CREATE record
# -------------------------------
@router.post("/")
def create_record(record: TrafficRecord):
    result = collection.insert_one(record.dict())
    return {"inserted_id": str(result.inserted_id)}

# -------------------------------
# UPDATE record
# -------------------------------
@router.put("/")
def update_record(date_time: datetime, traffic_volume: int):
    result = collection.update_one({"date_time": date_time}, {"$set": {"traffic_volume": traffic_volume}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"modified_count": result.modified_count}

# -------------------------------
# DELETE record
# -------------------------------
@router.delete("/")
def delete_record(date_time: datetime):
    result = collection.delete_one({"date_time": date_time})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"deleted_count": result.deleted_count}

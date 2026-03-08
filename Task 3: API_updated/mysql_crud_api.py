# mysql_crud_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd

router = APIRouter(prefix="/mysql", tags=["MySQL"])

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DB = os.getenv("MYSQL_DB")

engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")


# -------------------------------
# Pydantic model for traffic record
# -------------------------------
class TrafficRecord(BaseModel):
    traffic_volume: int
    rain_1h: float
    snow_1h: float
    clouds_all: int
    lag_1: float = None
    lag_24: float = None
    lag_168: float = None
    rolling_mean_24: float = None
    rolling_mean_168: float = None
    datetime_id: int
    holiday_id: int
    weather_id: int


# -------------------------------
# GET full dataset
# -------------------------------
@router.get("/all")
def get_all():
    query = text("""
    SELECT t.primary_id, t.traffic_volume, t.temp, t.rain_1h, t.snow_1h, t.clouds_all, t.lag_1, t.lag_24,
        t.lag_168, t.rolling_mean_24, t.rolling_mean_168,
        d.date_time, d.year, d.month, d.day, d.hour, d.day_of_week, d.is_weekend, 
        h.holiday, w.weather_main
    FROM traffic t
    JOIN datetime_info d ON t.datetime_id = d.datetime_id
    JOIN holiday_info h ON t.holiday_id = h.holiday_id
    JOIN weather_info w ON t.weather_id = w.weather_id;
    """)
    df = pd.read_sql(query, engine)
    if df.empty:
        raise HTTPException(status_code=404, detail="No records found")
    return df.to_dict(orient="records")


# -------------------------------
# GET latest record
# -------------------------------
@router.get("/latest")
def get_latest():
    query = text("SELECT * FROM traffic ORDER BY primary_id DESC LIMIT 1")
    df = pd.read_sql(query, engine)
    if df.empty:
        raise HTTPException(status_code=404, detail="No records found")
    return df.to_dict(orient="records")[0]


# -------------------------------
# GET records by date range
# -------------------------------
@router.get("/range")
def get_by_range(start: str, end: str):
    query = text("""
    SELECT *
    FROM traffic t
    JOIN datetime_info d ON t.datetime_id = d.datetime_id
    WHERE d.date_time BETWEEN :start AND :end
    """)
    df = pd.read_sql(query, engine, params={"start": start, "end": end})
    return df.to_dict(orient="records")


# -------------------------------
# GET single record by datetime
# -------------------------------
@router.get("/single")
def get_single(date_time: str):
    query = text("""
    SELECT t.primary_id, t.traffic_volume, t.temp, t.rain_1h, t.snow_1h, t.clouds_all, t.lag_1, t.lag_24,
            t.lag_168, t.rolling_mean_24, t.rolling_mean_168,
            d.date_time, d.year, d.month, d.day, d.hour, d.day_of_week, d.is_weekend, 
            h.holiday, w.weather_main
    FROM traffic t
    JOIN datetime_info d ON t.datetime_id = d.datetime_id
    JOIN holiday_info h ON t.holiday_id = h.holiday_id
    JOIN weather_info w ON t.weather_id = w.weather_id
    WHERE d.date_time = :dt
    """)
    df = pd.read_sql(query, engine, params={"dt": date_time})
    if df.empty:
        raise HTTPException(status_code=404, detail="Record not found")
    return df.to_dict(orient="records")[0]


# -------------------------------
# GET last 24 records leading up to a given datetime
# -------------------------------
@router.get("/last24")
def get_last_24(date_time: str):
    """
    Returns the last 24 records leading up to the given datetime.
    The first record in the list will be the desired date, going backwards.
    """
    query = text("""
    SELECT t.primary_id, t.traffic_volume, t.temp, t.rain_1h, t.snow_1h, t.clouds_all,
           t.lag_1, t.lag_24, t.lag_168, t.rolling_mean_24, t.rolling_mean_168,
           d.date_time, d.year, d.month, d.day, d.hour, d.day_of_week, d.is_weekend,
           h.holiday, w.weather_main
    FROM traffic t
    JOIN datetime_info d ON t.datetime_id = d.datetime_id
    JOIN holiday_info h ON t.holiday_id = h.holiday_id
    JOIN weather_info w ON t.weather_id = w.weather_id
    WHERE d.date_time <= :dt
    ORDER BY d.date_time DESC
    LIMIT 24
    """)

    df = pd.read_sql(query, engine, params={"dt": date_time})

    if df.empty or len(df) < 24:
        raise HTTPException(status_code=404, detail="Not enough records (need 24)")

    # Return as list of dicts, first item is desired date, going backwards
    return df.to_dict(orient="records")

# -------------------------------
# CREATE record
# -------------------------------
@router.post("/")
def create_record(record: TrafficRecord):
    query = text("""
    INSERT INTO traffic (traffic_volume, rain_1h, snow_1h, clouds_all,
                         lag_1, lag_24, lag_168, rolling_mean_24, rolling_mean_168,
                         datetime_id, holiday_id, weather_id)
    VALUES (:traffic_volume, :rain_1h, :snow_1h, :clouds_all,
            :lag_1, :lag_24, :lag_168, :rolling_mean_24, :rolling_mean_168,
            :datetime_id, :holiday_id, :weather_id)
    """)
    with engine.begin() as conn:
        conn.execute(query, record.dict())
    return {"message": "Record created successfully"}


# -------------------------------
# UPDATE record
# -------------------------------
@router.put("/{primary_id}")
def update_record(primary_id: int, record: TrafficRecord):
    query = text("""
    UPDATE traffic SET
        traffic_volume = :traffic_volume,
        rain_1h = :rain_1h,
        snow_1h = :snow_1h,
        clouds_all = :clouds_all,
        lag_1 = :lag_1,
        lag_24 = :lag_24,
        lag_168 = :lag_168,
        rolling_mean_24 = :rolling_mean_24,
        rolling_mean_168 = :rolling_mean_168,
        datetime_id = :datetime_id,
        holiday_id = :holiday_id,
        weather_id = :weather_id
    WHERE primary_id = :primary_id
    """)
    with engine.begin() as conn:
        result = conn.execute(query, {**record.dict(), "primary_id": primary_id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record updated successfully"}


# -------------------------------
# DELETE record
# -------------------------------
@router.delete("/{primary_id}")
def delete_record(primary_id: int):
    query = text("DELETE FROM traffic WHERE primary_id = :primary_id")
    with engine.begin() as conn:
        result = conn.execute(query, {"primary_id": primary_id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}
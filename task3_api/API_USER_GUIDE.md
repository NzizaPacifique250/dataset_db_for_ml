# Traffic Volume API - User Guide

## Overview

This comprehensive REST API provides CRUD operations and time-series query endpoints for traffic volume data stored in both SQL (MySQL) and NoSQL (MongoDB) databases. The API is built with Flask and supports complete data manipulation capabilities across both database systems.

## Table of Contents

1. [Setup & Installation](#setup--installation)
2. [API Endpoints](#api-endpoints)
3. [Authentication & Headers](#authentication--headers)
4. [Usage Examples](#usage-examples)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)
7. [Integration with Other Tasks](#integration-with-other-tasks)

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- PyMongo 4.6.0
- MySQL Server running locally (for SQL operations)
- MongoDB running locally or MongoDB Atlas (for MongoDB operations)

### Installation Steps

#### 1. Navigate to the API directory
```bash
cd task3_api
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Database Connections

**For MySQL:**
- Ensure MySQL Server 8.x is running
- Update the `SQLALCHEMY_DATABASE_URI` in `config.py` if your connection differs:
  ```python
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/traffic_db'
  ```

**For MongoDB (Local):**
- Ensure MongoDB is running: `net start MongoDB` (Windows) or `brew services start mongodb-community` (macOS)
- Default connection: `mongodb://localhost:27017/traffic_db`

**For MongoDB (Atlas Cloud):**
- Update `MONGO_URI` in `config.py`:
  ```python
  MONGO_URI = 'mongodb+srv://<DB_USER>:<DB_PASSWORD>@<CLUSTER_HOST>/traffic_db'
  ```

#### 4. Run the Application
```bash
python app.py
```

The API will start on `http://localhost:5000`

#### 5. Verify Installation
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "services": {
    "api": "running",
    "sql": "connected",
    "mongodb": "connected"
  }
}
```

---

## API Endpoints

### Endpoint Structure

The API uses the following structure:
- **SQL endpoints**: `/api/v1/sql/...`
- **MongoDB endpoints**: `/api/v1/mongodb/...`

### SQL Database Endpoints

#### Traffic Records - CRUD Operations

##### 1. Create Traffic Record (POST)
```http
POST /api/v1/sql/traffic
Content-Type: application/json

{
  "date_time": "2013-06-01T09:00:00",
  "temp": 288.5,
  "rain_1h": 0.0,
  "snow_1h": 0.0,
  "clouds_all": 40,
  "traffic_volume": 5545,
  "holiday_id": null,
  "weather_id": 1
}
```

**Response (201):**
```json
{
  "message": "Traffic record created successfully",
  "record": {
    "record_id": 48199,
    "date_time": "2013-06-01T09:00:00",
    "temp": 288.5,
    "rain_1h": 0.0,
    "snow_1h": 0.0,
    "clouds_all": 40,
    "traffic_volume": 5545,
    "holiday_id": null,
    "weather_id": 1,
    "holiday_name": null,
    "weather_main": "Clouds",
    "weather_description": "scattered clouds"
  }
}
```

##### 2. Get All Traffic Records (GET)
```http
GET /api/v1/sql/traffic?page=1&per_page=20
```

**Response (200):**
```json
{
  "total": 48198,
  "page": 1,
  "per_page": 20,
  "pages": 2410,
  "data": [
    {
      "record_id": 1,
      "date_time": "2012-10-02T09:00:00",
      "temp": 288.28,
      "traffic_volume": 5545,
      "weather_main": "Clouds",
      "weather_description": "scattered clouds",
      "holiday_name": null
    },
    ...
  ]
}
```

##### 3. Get Traffic Record by ID (GET)
```http
GET /api/v1/sql/traffic/1
```

**Response (200):**
```json
{
  "record_id": 1,
  "date_time": "2012-10-02T09:00:00",
  "temp": 288.28,
  "rain_1h": 0.0,
  "snow_1h": 0.0,
  "clouds_all": 40,
  "traffic_volume": 5545,
  "holiday_id": null,
  "weather_id": 1,
  "holiday_name": null,
  "weather_main": "Clouds",
  "weather_description": "scattered clouds"
}
```

##### 4. Update Traffic Record (PUT)
```http
PUT /api/v1/sql/traffic/1
Content-Type: application/json

{
  "traffic_volume": 5600,
  "temp": 290.5
}
```

**Response (200):**
```json
{
  "message": "Traffic record updated successfully",
  "record": {
    "record_id": 1,
    "date_time": "2012-10-02T09:00:00",
    "traffic_volume": 5600,
    "temp": 290.5,
    ...
  }
}
```

##### 5. Delete Traffic Record (DELETE)
```http
DELETE /api/v1/sql/traffic/1
```

**Response (200):**
```json
{
  "message": "Traffic record deleted successfully"
}
```

#### Time-Series Specific Endpoints

##### 6. Get Latest Record (GET)
```http
GET /api/v1/sql/traffic/latest
```

**Response (200):**
```json
{
  "message": "Latest traffic record",
  "record": {
    "record_id": 48198,
    "date_time": "2014-09-30T23:00:00",
    "temp": 282.0,
    "traffic_volume": 1680,
    "weather_main": "Clouds",
    "weather_description": "few clouds",
    "holiday_name": null
  }
}
```

##### 7. Get Records by Date Range (GET)
```http
GET /api/v1/sql/traffic/date-range?start_date=2013-06-01T00:00:00&end_date=2013-06-02T23:59:59
```

**Response (200):**
```json
{
  "start_date": "2013-06-01T00:00:00",
  "end_date": "2013-06-02T23:59:59",
  "record_count": 48,
  "records": [
    {
      "record_id": 12345,
      "date_time": "2013-06-01T00:00:00",
      "temp": 285.5,
      "traffic_volume": 4200,
      "weather_main": "Rain",
      "weather_description": "light rain",
      "holiday_name": null
    },
    ...
  ]
}
```

#### Holiday Management - CRUD Operations

##### 8. Create Holiday (POST)
```http
POST /api/v1/sql/holidays
Content-Type: application/json

{
  "holiday_name": "New Year's Day"
}
```

**Response (201):**
```json
{
  "message": "Holiday created successfully",
  "holiday": {
    "holiday_id": 12,
    "holiday_name": "New Year's Day"
  }
}
```

##### 9. Get All Holidays (GET)
```http
GET /api/v1/sql/holidays
```

**Response (200):**
```json
[
  {
    "holiday_id": 1,
    "holiday_name": "New Year's Day"
  },
  {
    "holiday_id": 2,
    "holiday_name": "Independence Day"
  },
  ...
]
```

##### 10. Update Holiday (PUT)
```http
PUT /api/v1/sql/holidays/1
Content-Type: application/json

{
  "holiday_name": "New Year's Day (Updated)"
}
```

##### 11. Delete Holiday (DELETE)
```http
DELETE /api/v1/sql/holidays/1
```

---

### MongoDB Database Endpoints

#### Traffic Records - CRUD Operations

##### 1. Create Traffic Record (POST)
```http
POST /api/v1/mongodb/traffic
Content-Type: application/json

{
  "date_time": "2013-06-01T09:00:00Z",
  "traffic_volume": 5545,
  "weather": {
    "main": "Clouds",
    "description": "scattered clouds",
    "temp": 288.28,
    "rain_1h": 0.0,
    "snow_1h": 0.0,
    "clouds_all": 40
  },
  "holiday": null
}
```

**Response (201):**
```json
{
  "message": "Traffic record created successfully",
  "id": "507f1f77bcf86cd799439011",
  "record": {
    "date_time": "2013-06-01T09:00:00+00:00",
    "traffic_volume": 5545,
    "weather": {
      "main": "Clouds",
      "description": "scattered clouds",
      "temp": 288.28,
      "rain_1h": 0.0,
      "snow_1h": 0.0,
      "clouds_all": 40
    },
    "holiday": null
  }
}
```

##### 2. Get All Traffic Records (GET)
```http
GET /api/v1/mongodb/traffic?page=1&per_page=20
```

**Response (200):**
```json
{
  "total": 48198,
  "page": 1,
  "per_page": 20,
  "pages": 2410,
  "data": [
    {
      "date_time": "2014-09-30T23:00:00+00:00",
      "traffic_volume": 1680,
      "weather": {
        "main": "Clouds",
        "description": "few clouds",
        "temp": 282.0,
        "rain_1h": 0.0,
        "snow_1h": 0.0,
        "clouds_all": 20
      },
      "holiday": null
    },
    ...
  ]
}
```

##### 3. Get Traffic Record by ID (GET)
```http
GET /api/v1/mongodb/traffic/507f1f77bcf86cd799439011
```

**Response (200):**
```json
{
  "date_time": "2013-06-01T09:00:00+00:00",
  "traffic_volume": 5545,
  "weather": {
    "main": "Clouds",
    "description": "scattered clouds",
    "temp": 288.28,
    "rain_1h": 0.0,
    "snow_1h": 0.0,
    "clouds_all": 40
  },
  "holiday": null
}
```

##### 4. Update Traffic Record (PUT)
```http
PUT /api/v1/mongodb/traffic/507f1f77bcf86cd799439011
Content-Type: application/json

{
  "traffic_volume": 5600
}
```

**Response (200):**
```json
{
  "message": "Traffic record updated successfully",
  "record": {
    "date_time": "2013-06-01T09:00:00+00:00",
    "traffic_volume": 5600,
    "weather": {...},
    "holiday": null
  }
}
```

##### 5. Delete Traffic Record (DELETE)
```http
DELETE /api/v1/mongodb/traffic/507f1f77bcf86cd799439011
```

**Response (200):**
```json
{
  "message": "Traffic record deleted successfully"
}
```

#### Time-Series Specific Endpoints

##### 6. Get Latest Record (GET)
```http
GET /api/v1/mongodb/traffic/latest
```

**Response (200):**
```json
{
  "message": "Latest traffic record",
  "record": {
    "date_time": "2014-09-30T23:00:00+00:00",
    "traffic_volume": 1680,
    "weather": {
      "main": "Clouds",
      "description": "few clouds",
      "temp": 282.0,
      "clouds_all": 20
    },
    "holiday": null
  }
}
```

##### 7. Get Records by Date Range (GET)
```http
GET /api/v1/mongodb/traffic/date-range?start_date=2013-06-01T00:00:00Z&end_date=2013-06-02T23:59:59Z
```

**Response (200):**
```json
{
  "start_date": "2013-06-01T00:00:00Z",
  "end_date": "2013-06-02T23:59:59Z",
  "record_count": 48,
  "records": [
    {
      "date_time": "2013-06-01T00:00:00+00:00",
      "traffic_volume": 4200,
      "weather": {...},
      "holiday": null
    },
    ...
  ]
}
```

---

## Authentication & Headers

Currently, the API does not require authentication. For production environments, consider adding:

- **API Keys**: Add an authentication layer for API key validation
- **JWT Tokens**: Implement token-based authentication
- **OAuth 2.0**: For third-party integrations

### Request Headers

```http
Content-Type: application/json
```

### Response Headers

```http
Content-Type: application/json
```

---

## Usage Examples

### Example 1: Create and Retrieve a Record

**Step 1: Create a new traffic record (SQL)**
```bash
curl -X POST http://localhost:5000/api/v1/sql/traffic \
  -H "Content-Type: application/json" \
  -d '{
    "date_time": "2024-01-15T10:00:00",
    "temp": 290.5,
    "rain_1h": 0.0,
    "traffic_volume": 5800,
    "weather_id": 1
  }'
```

**Step 2: Get the latest record**
```bash
curl http://localhost:5000/api/v1/sql/traffic/latest
```

### Example 2: Date Range Query for Analytics

**Query traffic volume for a specific month (MongoDB)**
```bash
curl "http://localhost:5000/api/v1/mongodb/traffic/date-range?start_date=2013-06-01T00:00:00Z&end_date=2013-06-30T23:59:59Z"
```

### Example 3: Update Records with New Weather Data

**Update a record with corrected weather information**
```bash
curl -X PUT http://localhost:5000/api/v1/sql/traffic/12345 \
  -H "Content-Type: application/json" \
  -d '{
    "temp": 292.0,
    "clouds_all": 50,
    "traffic_volume": 6100
  }'
```

### Example 4: Delete Obsolete Holiday Entry

**Remove a holiday that was incorrectly added**
```bash
curl -X DELETE http://localhost:5000/api/v1/sql/holidays/15
```

---

## Response Formats

### Success Response (200, 201)
```json
{
  "message": "Operation message",
  "data": {
    "field": "value"
  }
}
```

### Error Response (400, 404, 500)
```json
{
  "error": "Error description"
}
```

### Pagination Response
```json
{
  "total": 48198,
  "page": 1,
  "per_page": 20,
  "pages": 2410,
  "data": [...]
}
```

---

## Error Handling

### Common HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Missing required fields |
| 404 | Not Found | Record doesn't exist |
| 500 | Server Error | Database connection issues |

### Error Examples

**Missing Required Field:**
```json
{
  "error": "Missing required fields: date_time, traffic_volume, weather_id"
}
```

**Record Not Found:**
```json
{
  "error": "Record not found"
}
```

**Database Connection Error:**
```json
{
  "error": "MongoDB connection not available"
}
```

---

## Integration with Other Tasks

### How Task 3 Integrates with the Complete ML Pipeline

#### **Task 1: Preprocessing & EDA (Data Analysis)**
- The API provides access to raw and processed time-series data
- Date range queries enable fetching specific periods for analysis
- Latest record endpoint supports real-time monitoring

#### **Task 2: Database Design**
- The API directly uses the schema designed in Task 2
- Implements all 3 SQL tables (holidays, weather_conditions, traffic_records)
- Leverages MongoDB collection structure with nested documents

#### **Task 4: Prediction Script**
The Task 4 prediction script will:
1. **Fetch data** using the API date-range endpoints:
   ```python
   response = requests.get(
       'http://localhost:5000/api/v1/sql/traffic/date-range',
       params={
           'start_date': '2013-01-01',
           'end_date': '2013-12-31'
       }
   )
   data = response.json()['records']
   ```

2. **Preprocess** using the same pipeline as Task 1
3. **Make predictions** with the trained model
4. **Update database** by creating new records with API POST endpoint

### Workflow Integration Diagram

```
┌──────────────┐
│   Task 1: EDA│──────────┐
│ & Modeling   │          │ Training Data & Features
└──────────────┘          │
                          ▼
                    ┌──────────────┐
                    │  Trained     │
                    │  Model File  │
                    └──────────────┘
                          │
     Predictions, Features │
                          ▼
┌──────────────┐    ┌──────────────┐
│   API Fetch  │───▶│  Task 3: API │◀────┐
│  Data Points │    │   Endpoints  │     │
│  (Task 4)    │    └──────────────┘     │
└──────────────┘          ▲               │
                          │ CRUD & TS    │
     ┌────────────────────┴─────────┐    │
     │                              │    │
     ▼                              ▼    │
┌──────────────┐         ┌──────────────┐
│   Task 2:    │         │   Task 2:    │
│   MySQL DB   │         │  MongoDB DB  │
└──────────────┘         └──────────────┘
```

### Example: Complete Data Pipeline

**1. Fetch last 7 days of data for prediction (Task 4)**
```python
import requests
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

response = requests.get(
    'http://localhost:5000/api/v1/sql/traffic/date-range',
    params={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }
)
recent_data = response.json()['records']
```

**2. Preprocess data using Task 1 pipeline**
```python
from preprocessing import clean_data, create_features  # From Task 1

X = clean_data(recent_data)
X = create_features(X)
```

**3. Make prediction with trained model**
```python
from joblib import load

model = load('trained_model.pkl')
prediction = model.predict(X)
```

**4. Store prediction results**
```python
prediction_record = {
    'date_time': datetime.now(),
    'traffic_volume': int(prediction[0]),
    'weather': {...},
    'holiday': None
}

requests.post(
    'http://localhost:5000/api/v1/mongodb/traffic',
    json=prediction_record
)
```

---

## Troubleshooting

### Issue: "MongoDB connection not available"
**Solution:**
- Ensure MongoDB is running: `net start MongoDB`
- Verify connection string in `config.py`
- Check MongoDB Atlas URI format if using cloud

### Issue: "Record not found"
**Solution:**
- Verify the record ID exists
- Check the database contains data
- Run database initialization scripts

### Issue: "Missing required field: weather_id"
**Solution:**
- Ensure weather_id exists in weather_conditions table (SQL)
- Provide all required fields in request body
- Check API documentation for required fields

### Issue: CORS Errors (when called from web frontend)
**Solution:**
Add Flask-CORS to handle cross-origin requests:
```python
from flask_cors import CORS
CORS(app)
```

---

## Support & Documentation

For more information:
- Check `README.md` in the root directory
- Review database schema in `SETUP_GUIDE.md`
- Consult task-specific documentation files

---

**API Version:** 1.0.0  
**Last Updated:** January 2024  
**Maintained by:** Kayonga Elvis

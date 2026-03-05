# API Architecture & Workflow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATIONS                         │
│  (Web Browser, Mobile App, Python Script, Task 4 Prediction)    │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP Requests / JSON Responses
                     │
         ┌───────────▼────────────┐
         │   Flask REST API       │
         │   (app.py)             │
         │                        │
         │ ┌────────────────────┐ │
         │ │  Route Handlers    │ │
         │ │  - CRUD endpoints  │ │
         │ │  - Time-series     │ │
         │ │  - Error handling  │ │
         │ └────────────────────┘ │
         │                        │
         │ ┌────────────────────┐ │
         │ │  SQLAlchemy ORM    │ │
         │ │  - Models          │ │
         │ │  - Sessions        │ │
         │ └────────────────────┘ │
         │                        │
         │ ┌────────────────────┐ │
         │ │  PyMongo Driver    │ │
         │ │  - Collections     │ │
         │ │  - Aggregation     │ │
         │ └────────────────────┘ │
         └────┬───────────────┬───┘
              │               │
    ┌─────────▼──┐    ┌──────▼────────┐
    │   MySQL    │    │   MongoDB     │
    │            │    │               │
    │ Tables:    │    │ Collections:  │
    │ ─holidays  │    │ ─traffic_data │
    │ ─weather   │    │               │
    │ ─traffic   │    │ 48,198 docs   │
    │            │    │               │
    │ 48K+ rows  │    │ Indexes:      │
    │            │    │ ─date_time    │
    │ Indexes:   │    │ ─weather.main │
    │ ─date_time │    │ ─holiday      │
    │ ─traffic   │    │               │
    └────────────┘    └───────────────┘
```

---

## API Request/Response Flow

```
CLIENT REQUEST
    │
    ├─ HTTP Method (GET, POST, PUT, DELETE)
    ├─ Endpoint (/api/v1/sql/traffic)
    ├─ Headers (Content-Type: application/json)
    └─ Body (optional - JSON data)
             │
             ▼
    FLASK ROUTE HANDLER
             │
             ├─ Parse request data
             ├─ Validate input
             ├─ Type conversion (DateTime parsing)
             │
             ├─ SQL Path ────┐ MongoDB Path
             │               │
             ▼               ▼
        SQLAlchemy      PyMongo Client
        ORM Query       (Aggregation/Query)
             │               │
             │               │
        ┌────▼────┐    ┌─────▼────┐
        │  MySQL  │    │ MongoDB   │
        └────┬────┘    └─────┬────┘
             │               │
             └───────┬───────┘
                     │
                RESULT DATA
                     │
    ┌────────────────▼───────────────┐
    │  Format Response               │
    │  ├─ Status Code (200, 201, etc)│
    │  ├─ JSON Body                  │
    │  ├─ Error messages (if any)    │
    │  └─ Metadata (pagination, etc) │
    └────────────────┬───────────────┘
                     │
                     ▼
            CLIENT RECEIVES RESPONSE
```

---

## Endpoint Categories

```
┌─────────────────────────────────────────────────────────┐
│                   REST API ENDPOINTS                     │
└─────────────────────────────────────────────────────────┘
        │
        ├─ /api/health ────────────────► Health Check
        │
        ├─ /api/v1 ────────────────────► API Information
        │
        ├─────────────────────────────────────────────┐
        │          SQL ENDPOINTS                      │
        │       (/api/v1/sql/...)                     │
        │                                             │
        │  ┌── TRAFFIC CRUD (5) ─────────────┐       │
        │  │  POST   /traffic               │       │
        │  │  GET    /traffic               │       │
        │  │  GET    /traffic/<id>          │       │
        │  │  PUT    /traffic/<id>          │       │
        │  │  DELETE /traffic/<id>          │       │
        │  └────────────────────────────────┘       │
        │                                             │
        │  ┌── TIME-SERIES (2) ──────────────┐       │
        │  │  GET    /traffic/latest        │       │
        │  │  GET    /traffic/date-range    │       │
        │  └────────────────────────────────┘       │
        │                                             │
        │  ┌── HOLIDAYS CRUD (4) ────────────┐       │
        │  │  POST   /holidays               │       │
        │  │  GET    /holidays               │       │
        │  │  PUT    /holidays/<id>          │       │
        │  │  DELETE /holidays/<id>          │       │
        │  └────────────────────────────────┘       │
        │                                             │
        └─────────────────────────────────────────────┘
        │
        ├─────────────────────────────────────────────┐
        │       MONGODB ENDPOINTS                     │
        │    (/api/v1/mongodb/...)                    │
        │                                             │
        │  ┌── TRAFFIC CRUD (5) ─────────────┐       │
        │  │  POST   /traffic               │       │
        │  │  GET    /traffic               │       │
        │  │  GET    /traffic/<id>          │       │
        │  │  PUT    /traffic/<id>          │       │
        │  │  DELETE /traffic/<id>          │       │
        │  └────────────────────────────────┘       │
        │                                             │
        │  ┌── TIME-SERIES (2) ──────────────┐       │
        │  │  GET    /traffic/latest        │       │
        │  │  GET    /traffic/date-range    │       │
        │  └────────────────────────────────┘       │
        │                                             │
        └─────────────────────────────────────────────┘
        │
        └─► TOTAL: 14 Endpoints
```

---

## CRUD Operation Matrix

```
        GET     POST    PUT     DELETE
        (Read)  (Create)(Update)(Delete)
        ─────   ──────  ─────   ──────

SQL
Traffic  ✓       ✓       ✓       ✓
Holiday  ✓       ✓       ✓       ✓

MongoDB
Traffic  ✓       ✓       ✓       ✓

Time-Series Operations:
SQL
Latest   ✓       ✗       ✗       ✗
Date-Range ✓    ✗       ✗       ✗

MongoDB
Latest   ✓       ✗       ✗       ✗
Date-Range ✓    ✗       ✗       ✗
```

---

## Data Flow: Task Integration Example

```
┌──────────────────┐
│  Raw CSV Data    │
│  48,198 records  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  TASK 1: Analysis    │
│  & Modeling          │
│ ✓ EDA               │
│ ✓ Feature Eng.      │
│ ✓ Train Model       │
└────────┬─────────────┘
         │
   ┌─────┴────────┐
   │              │
   ▼              ▼
Trained   Preprocessing
Model     Pipeline
   │              │
   │    ┌─────────│
   │    │         ▼
   │    │  ┌──────────────────────┐
   │    └─▶│  TASK 2: Database    │
   │       │  Design              │
   │       │ ✓ SQL Schema         │
   │       │ ✓ MongoDB Setup      │
   │       │ ✓ Data Loading       │
   │       └──────┬───────────────┘
   │              │
   │              ▼
   │       ┌──────────────────────┐
   │       │  TASK 3: API         │
   │       │ ✓ 14 endpoints       │
   │       │ ✓ CRUD operations    │
   │       │ ✓ Time-series        │
   │       └──────┬───────────────┘
   │              │
   │    ┌─────────┴─────────┐
   │    │                   │
   │    ▼                   ▼
   │  Data Fetch      Prediction Storage
   │  (date-range)    (create record)
   │    │                   │
   │    └─────────┬─────────┘
   │              │
   └──────────────┼──────────────┐
                  │              │
                  ▼              ▼
           ┌──────────────────────┐
           │  TASK 4: Prediction  │
           │  Script              │
           │ ✓ Fetch data         │
           │ ✓ Preprocess         │
           │ ✓ Load model         │
           │ ✓ Predict            │
           │ ✓ Store results      │
           └──────────────────────┘
```

---

## Time-Series Operations Detail

### Latest Record Flow

```
CLIENT REQUEST: GET /api/v1/sql/traffic/latest

Flask Handler:
    ↓
SQLAlchemy Query:
    TrafficRecord.query.order_by(date_time DESC).first()
    ↓
MySQL:
    SELECT * FROM traffic_records
    ORDER BY date_time DESC
    LIMIT 1
    ↓
Response:
    {
        "message": "Latest traffic record",
        "record": {
            "record_id": 48198,
            "date_time": "2014-09-30T23:00:00",
            "traffic_volume": 1680,
            "weather_main": "Clouds",
            ...
        }
    }
```

### Date-Range Query Flow

```
CLIENT REQUEST:
GET /api/v1/sql/traffic/date-range?start_date=2013-06-01&end_date=2013-06-30

Parse Parameters:
    start_date = DateTime("2013-06-01T00:00:00")
    end_date = DateTime("2013-06-30T23:59:59")
    ↓
SQLAlchemy Query:
    TrafficRecord.query.filter(
        date_time >= start_date,
        date_time <= end_date
    ).order_by(date_time).all()
    ↓
MySQL:
    SELECT * FROM traffic_records
    WHERE date_time >= '2013-06-01 00:00:00'
      AND date_time <= '2013-06-30 23:59:59'
    ORDER BY date_time
    ↓
Response:
    {
        "start_date": "2013-06-01T00:00:00",
        "end_date": "2013-06-30T23:59:59",
        "record_count": 720,
        "records": [
            {...},
            {...},
            ...
        ]
    }
```

---

## Error Handling Flow

```
CLIENT REQUEST
    ↓
VALIDATION
    ├─ Missing required field?
    │  ↓
    │  ✗ Return 400 Bad Request
    │    {"error": "Missing required fields: ..."}
    │
    ├─ Invalid record ID?
    │  ↓
    │  ✗ Return 404 Not Found
    │    {"error": "Record not found"}
    │
    └─ Proceed to database operation
         ↓
    DATABASE OPERATION
         ├─ Connection error?
         │  ↓
         │  ✗ Return 500 Server Error
         │    {"error": "MongoDB connection not available"}
         │
         ├─ Query fails?
         │  ↓
         │  ✗ Return 500 Server Error
         │    {"error": "<specific error message>"}
         │
         └─ Success
              ↓
              ✓ Return appropriate status
                (200, 201, etc.)
```

---

## Database Connection Management

```
┌─────────────────────────────────────────┐
│  Flask Application Initialization        │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   SQLAlchemy           PyMongo Client
   Initialize           Initialize
        │                         │
        │ Create Engine           │ Create Connection
        │                         │
        ▼                         ▼
   MySQL Pool            MongoDB Connection
   (mysql+pymysql)       Pool
        │                         │
        └─────────┬───────────────┘
                  │
           ✓ Ready for Requests
                  │
        ┌─────────┴────────────┐
        │                      │
        ▼                      ▼
    SQL Query            MongoDB Query
    (with ORM)           (with aggregation)
        │                      │
        │                      │
    ✓ Success                 ✓ Success
```

---

## Response Format Examples

### Success Response (201 Created)
```json
{
  "message": "Traffic record created successfully",
  "record": {
    "record_id": 48199,
    "date_time": "2023-01-15T10:00:00",
    "traffic_volume": 5500,
    "temp": 290.5,
    "weather_main": "Clouds",
    "holiday_name": null
  }
}
```

### Paginated Response (200 OK)
```json
{
  "total": 48198,
  "page": 1,
  "per_page": 20,
  "pages": 2410,
  "data": [
    {...},
    {...}
  ]
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Missing required fields: date_time, traffic_volume, weather_id"
}
```

---

## Performance Optimization Features

```
┌──────────────────────────────────────────────┐
│        PERFORMANCE OPTIMIZATIONS              │
└──────────────────────────────────────────────┘
        │
        ├─ Database Indexing
        │  ├─ DateTime index (for date-range queries)
        │  ├─ Traffic volume index (for analytics)
        │  └─ Foreign key indexes
        │
        ├─ Pagination
        │  ├─ Default: 20 records per page
        │  ├─ Configurable per request
        │  └─ Prevents large dataset transfers
        │
        ├─ Connection Pooling
        │  ├─ Reuse database connections
        │  └─ Reduce connection overhead
        │
        ├─ Query Optimization
        │  ├─ Only select needed columns
        │  ├─ Use aggregation pipelines (MongoDB)
        │  └─ Filter at database level
        │
        └─ Response Format
           ├─ JSON compression (client-side)
           ├─ Exclude unnecessary fields
           └─ Relationship resolution in API
```

---

**Generated by:** Kayonga Elvis  
**Purpose:** Visual understanding of API architecture  
**Last Updated:** January 2024

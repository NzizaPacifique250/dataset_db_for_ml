# Task 3: FastAPI CRUD Endpoints Setup Guide

This API provides RESTful endpoints for querying traffic data from both MySQL and MongoDB databases.

## Prerequisites

Before running the API, ensure you have:
- ✅ Completed **Task 2** (databases must be set up and populated)
- ✅ MySQL server running
- ✅ MongoDB server running
- ✅ Python 3.9+ installed

## Setup Instructions

### 1. Navigate to Task 3 Directory
```bash
cd "Task 3_ API_updated"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)
- SQLAlchemy & PyMySQL (MySQL driver)
- PyMongo (MongoDB driver)
- python-dotenv (environment variables)

### 3. Configure Environment Variables

Create a `.env` file in the **project root directory** (not in Task 3 folder):

```env
# MySQL Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=traffic_db

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=traffic_db
```

### 4. Start the API Server
```bash
uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

### 5. Access API Documentation

Open your browser and visit:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Available Endpoints

### MySQL Routes (`/mysql`)
- `GET /mysql/all` - Get all records
- `GET /mysql/latest` - Get latest record
- `GET /mysql/single?date_time=YYYY-MM-DD%20HH:MM:SS` - Get single record
- `GET /mysql/range?start=YYYY-MM-DD&end=YYYY-MM-DD` - Get date range
- `GET /mysql/last24?date_time=YYYY-MM-DD%20HH:MM:SS` - Get last 24 records
- `POST /mysql/` - Create new record
- `PUT /mysql/{id}` - Update record
- `DELETE /mysql/{id}` - Delete record

### MongoDB Routes (`/mongo`)
- `GET /mongo/latest` - Get latest document
- `GET /mongo/single?date_time=YYYY-MM-DDTHH:MM:SS` - Get single document
- `GET /mongo/last24?date_time=YYYY-MM-DDTHH:MM:SS` - Get last 24 documents
- `GET /mongo/range?start=YYYY-MM-DDTHH:MM:SS&end=YYYY-MM-DDTHH:MM:SS` - Get range
- `POST /mongo/` - Create document
- `PUT /mongo/` - Update document
- `DELETE /mongo/` - Delete document

## Testing the API

### Example 1: Get Latest Record (MySQL)
```bash
curl http://127.0.0.1:8000/mysql/latest
```

### Example 2: Get Single Record by Datetime
```bash
curl "http://127.0.0.1:8000/mysql/single?date_time=2018-09-30%2019:00:00"
```

### Example 3: Get Date Range (MongoDB)
```bash
curl "http://127.0.0.1:8000/mongo/range?start=2018-09-01T00:00:00&end=2018-09-07T23:59:59"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Can't connect to MySQL` | Check MySQL is running and credentials in `.env` are correct |
| `Can't connect to MongoDB` | Verify MongoDB is running: `mongosh` or check service status |
| `404 errors on all routes` | Ensure databases are populated (run Task 2 scripts first) |
| Port 8000 already in use | Change port: `uvicorn main:app --reload --port 8001` |

## Stopping the Server

Press `CTRL+C` in the terminal where uvicorn is running.

---

**Lead Developer:** Kayonga Elvis  
**Task:** API Development & CRUD Operations
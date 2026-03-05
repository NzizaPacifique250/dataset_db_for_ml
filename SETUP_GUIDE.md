# Task 2: Setup & Running Guide

This guide covers how to run the SQL and MongoDB scripts both **locally** and using **MongoDB Atlas** (cloud).

---

## Part 1: Running MySQL Locally

### Prerequisites
- MySQL Server 8.x installed ([Download](https://dev.mysql.com/downloads/mysql/))
- Make sure the MySQL `bin` folder is in your PATH, or use the full path:
  ```
  "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
  ```

### Step 1: Enable Local File Loading
MySQL disables local file imports by default. Enable it:

```sql
-- Run this once in MySQL
SET GLOBAL local_infile = 1;
```

### Step 2: Update the CSV File Path
Open `sql/load_data.sql` and verify the `LOAD DATA LOCAL INFILE` path on line 87 points to your CSV file:

```sql
LOAD DATA LOCAL INFILE 'C:/Users/josue/Music/formative_1_ML_Pipeline/Metro_Interstate_Traffic_Volume.csv'
```

> **Note:** Use forward slashes `/` even on Windows.

### Step 3: Create the Database and Tables

```bash
mysql -u root < sql/schema.sql
```

If your root user has a password:
```bash
mysql -u root -p < sql/schema.sql
```

### Step 4: Load Data from CSV

```bash
mysql -u root --local-infile=1 < sql/load_data.sql
```

Expected output:
```
total_records: 48198
total_holidays: 11
total_weather_conditions: 37
```

### Step 5: Run SQL Queries

```bash
mysql -u root < sql/queries.sql
```

This runs all 4 queries and prints their results to the terminal.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `mysql: command not found` | Add MySQL bin to PATH or use full path: `"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"` |
| `ERROR 3948: Loading local data is disabled` | Run `SET GLOBAL local_infile = 1;` in MySQL first, and use `--local-infile=1` flag when connecting |
| `ERROR 1062: Duplicate entry` | The script was already run. Drop the database first: `mysql -u root -e "DROP DATABASE traffic_db;"` then re-run from Step 3 |

---

## Part 2: Running MongoDB Locally

### Prerequisites
- MongoDB Community Server installed ([Download](https://www.mongodb.com/try/download/community))
- MongoDB Shell (`mongosh`) installed ([Download](https://www.mongodb.com/try/download/shell))

### Step 1: Start MongoDB
Make sure the MongoDB service is running:
```bash
# Windows (run as Administrator)
net start MongoDB
```

### Step 2: Create Collection and Insert Sample Documents

```bash
mongosh < mongodb/collection_design.js
```

Expected output:
```
Documents inserted: 10
Sample document: { ... }
```

### Step 3: Run MongoDB Queries

```bash
mongosh < mongodb/queries.js
```

This runs all 4 queries and prints results to the terminal.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `mongosh: command not found` | Use full path: `"C:\Users\josue\AppData\Local\Programs\mongosh\mongosh.exe"` |
| `MongoServerError: connect ECONNREFUSED` | MongoDB service is not running. Start it with `net start MongoDB` |
| `Document failed validation` | The collection already exists with old schema. The script drops and recreates it automatically, so just re-run |

---

## Part 3: Using MongoDB Atlas (Cloud)

MongoDB Atlas is a free cloud-hosted MongoDB service. Use this if you don't want to install MongoDB locally.

### Step 1: Create an Atlas Account
1. Go to [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Click **Try Free** and sign up
3. Choose the **M0 Free Tier** (shared cluster)
4. Select a cloud provider and region (any works)
5. Click **Create Deployment**

### Step 2: Set Up Database Access
1. In the Atlas dashboard, go to **Database Access** (left sidebar)
2. Click **Add New Database User**
3. Set a username and password (e.g., `traffic_admin` / `yourpassword`)
4. Set **Database User Privileges** to **Read and Write to Any Database**
5. Click **Add User**

### Step 3: Set Up Network Access
1. Go to **Network Access** (left sidebar)
2. Click **Add IP Address**
3. Click **Allow Access from Anywhere** (for development) or add your specific IP
4. Click **Confirm**

### Step 4: Get Your Connection String
1. Go to **Database** (left sidebar)
2. Click **Connect** on your cluster
3. Choose **Drivers** (or **Shell**)
4. Copy the connection string. It looks like:
   ```
   mongodb+srv://traffic_admin:<password>@cluster0.xxxxx.mongodb.net/
   ```
5. Replace `<password>` with your actual password

### Step 5: Connect with mongosh
```bash
mongosh "mongodb+srv://traffic_admin:yourpassword@cluster0.xxxxx.mongodb.net/traffic_db"
```

### Step 6: Run the Scripts
Once connected, you can either:

**Option A — Run script files:**
```bash
mongosh "mongodb+srv://traffic_admin:yourpassword@cluster0.xxxxx.mongodb.net/traffic_db" < mongodb/collection_design.js
mongosh "mongodb+srv://traffic_admin:yourpassword@cluster0.xxxxx.mongodb.net/traffic_db" < mongodb/queries.js
```

**Option B — Use the Atlas UI:**
1. In the Atlas dashboard, click **Browse Collections**
2. Click **Create Database** → Database name: `traffic_db`, Collection name: `traffic_data`
3. Click **Insert Document** and paste the sample documents from `collection_design.js`
4. Use the **Aggregation** tab to run the aggregation queries from `queries.js`

### Step 7: Verify in Atlas Dashboard
1. Go to **Database** → **Browse Collections**
2. Select `traffic_db` → `traffic_data`
3. You should see 10 documents with the embedded weather structure
4. Use the filter bar to test queries, e.g.:
   ```json
   { "holiday": { "$ne": null } }
   ```
   This shows only holiday records.

---

## File Reference

```
task2_databases/
├── sql/
│   ├── schema.sql           -- Creates traffic_db with 3 tables
│   ├── load_data.sql         -- Loads CSV data into MySQL
│   ├── queries.sql           -- 4 SQL queries
│   ├── erd.txt               -- Text-based ERD
│   ├── erd_diagram.png       -- Visual ERD diagram
│   └── generate_erd.py       -- Script to regenerate ERD image
├── mongodb/
│   ├── collection_design.js  -- Creates collection + 10 sample docs
│   └── queries.js            -- 4 MongoDB queries
├── README.md                 -- Design rationale
└── SETUP_GUIDE.md            -- This file
```

# MySQL Setup Instructions for API Testing

## Current Status
✅ **MongoDB endpoints**: Fully functional (4/6 tests passing)  
❌ **MySQL endpoints**: Blocked - MySQL not installed on this system

## What's Working Now
The API server is running successfully with these working components:
- Health check endpoint (reports MySQL as "disconnected", MongoDB as "connected")
- All MongoDB CRUD operations (Create, Read, Update, Delete)
- MongoDB time-series queries (latest record, date-range queries)
- API documentation endpoint

## To Complete MySQL Setup

### Step 1: Install MySQL 8.x
Download and install MySQL Community Server:
- **Windows**: https://dev.mysql.com/downloads/mysql/
- During installation, set root password (or leave blank for no password)
- Ensure MySQL service starts automatically

### Step 2: Verify MySQL Installation
Open PowerShell as Administrator and test:
```powershell
# Check if MySQL service exists
Get-Service | Where-Object { $_.Name -match 'mysql' }

# Start MySQL service (if not running)
net start MySQL80  # Service name may vary (MySQL, MySQL80, etc.)

# Test MySQL client connection
& "C:\Program Files\MySQL\MySQL Server 8.x\bin\mysql.exe" -u root -e "SELECT VERSION();"
```

### Step 3: Load Database Schema and Data
From the workspace directory, run:

```powershell
cd "C:\Users\user\Desktop\dataset_db_for_ml"

# Set the MySQL path (adjust version number if needed)
$mysql = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"

# Create schema
& $mysql -u root < "task 2 databases\sql\schema.sql"

# Load data (requires local_infile enabled)
& $mysql -u root --local-infile=1 < "task 2 databases\sql\load_data.sql"

# Verify data loaded
& $mysql -u root -e "USE traffic_db; SELECT COUNT(*) FROM traffic_records;"
```

**Expected output**: `48198` records loaded

### Step 4: Restart API and Re-run Tests
```powershell
# Kill current API server (Ctrl+C in its terminal)

# Restart with MongoDB still running
c:/python312/python.exe task3_api/app.py

# In another terminal, run tests
c:/python312/python.exe task3_api/test_api.py
```

**Expected result**: `6/6` tests passing

## Troubleshooting

### "MySQL service not found"
- Check installed service name: `Get-Service | Where-Object { $_.DisplayName -match 'mysql' }`
- Try alternative names: `MySQL`, `MySQL80`, `MySQL84`

### "ERROR 3948: Loading local data is disabled"
Enable it first:
```sql
mysql -u root -e "SET GLOBAL local_infile = 1;"
```

### "Access denied for user 'root'"
If you set a password during installation:
```powershell
$mysql -u root -p < "task 2 databases\sql\schema.sql"
# Enter password when prompted
```

### "Can't connect to MySQL server on 'localhost'"
Ensure MySQL service is running:
```powershell
net start MySQL80
# Or check: Get-Service | Where-Object { $_.Name -match 'mysql' }
```

## Alternative: Quick MySQL Setup with Chocolatey
If you have Chocolatey package manager:
```powershell
# Install MySQL via Chocolatey (run as Administrator)
choco install mysql

# Initialize and start service
mysqld --initialize-insecure --user=mysql
net start MySQL
```

## Current API Test Results
```
Total: 4/6 tests passed

✓ Health Check (degraded status - MongoDB connected, MySQL disconnected)
✓ API Info
✗ SQL CRUD (MySQL not available)
✗ SQL Time-Series (MySQL not available)
✓ MongoDB CRUD
✓ MongoDB Time-Series
```

Once MySQL is installed and loaded with data, all 6/6 tests should pass.

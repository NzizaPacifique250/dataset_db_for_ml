"""
Simple test file to verify API endpoints are working
Run: python test_api.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/v1"

# ANSI colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
END = '\033[0m'

def test_health_check():
    """Test API health check"""
    print(f"\n{YELLOW}Testing Health Check...{END}")
    response = requests.get(f"{BASE_URL}/api/health")
    if response.status_code == 200:
        print(f"{GREEN}✓ Health check passed{END}")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print(f"{RED}✗ Health check failed{END}")
        return False

def test_api_info():
    """Test API info endpoint"""
    print(f"\n{YELLOW}Testing API Info...{END}")
    response = requests.get(f"{API_URL}")
    if response.status_code == 200:
        print(f"{GREEN}✓ API info retrieved{END}")
        endpoints = response.json()['endpoints']
        print(f"  Active SQL endpoints: {len(endpoints['sql']['traffic'])} + {len(endpoints['sql']['holidays'])}")
        print(f"  Active MongoDB endpoints: {len(endpoints['mongodb']['traffic'])}")
        return True
    else:
        print(f"{RED}✗ Failed to retrieve API info{END}")
        return False

def test_sql_crud():
    """Test SQL CRUD operations"""
    print(f"\n{YELLOW}Testing SQL CRUD Operations...{END}")
    
    # CREATE
    print("  Testing CREATE...")
    new_record = {
        "date_time": datetime.now().isoformat(),
        "temp": 290.5,
        "rain_1h": 0.0,
        "snow_1h": 0.0,
        "clouds_all": 40,
        "traffic_volume": 5500,
        "weather_id": 1
    }
    response = requests.post(f"{API_URL}/sql/traffic", json=new_record)
    if response.status_code == 201:
        print(f"  {GREEN}✓ Record created{END}")
        record = response.json()['record']
        record_id = record['record_id']
    else:
        print(f"  {RED}✗ Create failed{END}")
        return False
    
    # READ
    print("  Testing READ...")
    response = requests.get(f"{API_URL}/sql/traffic/{record_id}")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Record retrieved{END}")
    else:
        print(f"  {RED}✗ Read failed{END}")
        return False
    
    # UPDATE
    print("  Testing UPDATE...")
    update_data = {"traffic_volume": 5600}
    response = requests.put(f"{API_URL}/sql/traffic/{record_id}", json=update_data)
    if response.status_code == 200:
        print(f"  {GREEN}✓ Record updated{END}")
    else:
        print(f"  {RED}✗ Update failed{END}")
        return False
    
    # DELETE
    print("  Testing DELETE...")
    response = requests.delete(f"{API_URL}/sql/traffic/{record_id}")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Record deleted{END}")
    else:
        print(f"  {RED}✗ Delete failed{END}")
        return False
    
    return True

def test_sql_time_series():
    """Test SQL time-series endpoints"""
    print(f"\n{YELLOW}Testing SQL Time-Series Endpoints...{END}")
    
    # Latest record
    print("  Testing /latest...")
    response = requests.get(f"{API_URL}/sql/traffic/latest")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Latest record retrieved{END}")
        print(f"    Most recent: {response.json()['record']['date_time']}")
    else:
        print(f"  {RED}✗ Latest endpoint failed{END}")
        return False
    
    # Date range
    print("  Testing /date-range...")
    params = {
        'start_date': '2013-06-01T00:00:00',
        'end_date': '2013-06-01T23:59:59'
    }
    response = requests.get(f"{API_URL}/sql/traffic/date-range", params=params)
    if response.status_code == 200:
        count = response.json()['record_count']
        print(f"  {GREEN}✓ Date-range query returned {count} records{END}")
    else:
        print(f"  {RED}✗ Date-range endpoint failed{END}")
        return False
    
    return True

def test_mongodb_crud():
    """Test MongoDB CRUD operations"""
    print(f"\n{YELLOW}Testing MongoDB CRUD Operations...{END}")
    
    # CREATE
    print("  Testing CREATE...")
    new_record = {
        "date_time": datetime.now().isoformat() + "Z",
        "traffic_volume": 5500,
        "weather": {
            "main": "Clouds",
            "description": "scattered clouds",
            "temp": 290.5,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 40
        },
        "holiday": None
    }
    response = requests.post(f"{API_URL}/mongodb/traffic", json=new_record)
    if response.status_code == 201:
        print(f"  {GREEN}✓ Document created{END}")
        record_id = response.json()['id']
    else:
        print(f"  {RED}✗ Create failed{END}")
        print(f"    Error: {response.json()}")
        return False
    
    # READ
    print("  Testing READ...")
    response = requests.get(f"{API_URL}/mongodb/traffic/{record_id}")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Document retrieved{END}")
    else:
        print(f"  {RED}✗ Read failed{END}")
        return False
    
    # UPDATE
    print("  Testing UPDATE...")
    update_data = {"traffic_volume": 5600}
    response = requests.put(f"{API_URL}/mongodb/traffic/{record_id}", json=update_data)
    if response.status_code == 200:
        print(f"  {GREEN}✓ Document updated{END}")
    else:
        print(f"  {RED}✗ Update failed{END}")
        return False
    
    # DELETE
    print("  Testing DELETE...")
    response = requests.delete(f"{API_URL}/mongodb/traffic/{record_id}")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Document deleted{END}")
    else:
        print(f"  {RED}✗ Delete failed{END}")
        return False
    
    return True

def test_mongodb_time_series():
    """Test MongoDB time-series endpoints"""
    print(f"\n{YELLOW}Testing MongoDB Time-Series Endpoints...{END}")
    
    # Latest record
    print("  Testing /latest...")
    response = requests.get(f"{API_URL}/mongodb/traffic/latest")
    if response.status_code == 200:
        print(f"  {GREEN}✓ Latest document retrieved{END}")
        print(f"    Most recent: {response.json()['record']['date_time']}")
    else:
        print(f"  {RED}✗ Latest endpoint failed{END}")
        return False
    
    # Date range
    print("  Testing /date-range...")
    params = {
        'start_date': '2013-06-01T00:00:00Z',
        'end_date': '2013-06-01T23:59:59Z'
    }
    response = requests.get(f"{API_URL}/mongodb/traffic/date-range", params=params)
    if response.status_code == 200:
        count = response.json()['record_count']
        print(f"  {GREEN}✓ Date-range query returned {count} documents{END}")
    else:
        print(f"  {RED}✗ Date-range endpoint failed{END}")
        return False
    
    return True

def main():
    """Run all tests"""
    print(f"\n{'='*60}")
    print(f"{'Traffic Volume API - Test Suite':^60}")
    print(f"{'='*60}")
    
    try:
        results = []
        
        results.append(("Health Check", test_health_check()))
        results.append(("API Info", test_api_info()))
        results.append(("SQL CRUD", test_sql_crud()))
        results.append(("SQL Time-Series", test_sql_time_series()))
        results.append(("MongoDB CRUD", test_mongodb_crud()))
        results.append(("MongoDB Time-Series", test_mongodb_time_series()))
        
        # Summary
        print(f"\n{'='*60}")
        print(f"{'Test Summary':^60}")
        print(f"{'='*60}")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = f"{GREEN}PASS{END}" if result else f"{RED}FAIL{END}"
            print(f"{test_name:.<50} {status}")
        
        print(f"\nTotal: {GREEN}{passed}{END}/{total} tests passed")
        
        if passed == total:
            print(f"\n{GREEN}✓ All tests passed!{END}")
        else:
            print(f"\n{RED}✗ Some tests failed. Check the output above.{END}")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}✗ Connection Error: Could not connect to API at {BASE_URL}{END}")
        print(f"   Make sure the API is running: python app.py")
    except Exception as e:
        print(f"\n{RED}✗ Unexpected error: {str(e)}{END}")

if __name__ == "__main__":
    main()

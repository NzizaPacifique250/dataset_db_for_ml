"""
Traffic Volume API - CRUD Endpoints for SQL and MongoDB
Task 3: Create Endpoints for CRUD and Time-Series Queries
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
import os
import sys
from config import config

# Initialize Flask app and extensions
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# MongoDB connection
try:
    mongo_client = MongoClient(app.config['MONGO_URI'])
    mongo_db = mongo_client['traffic_db']
    traffic_collection = mongo_db['traffic_data']
except Exception as e:
    print(f"Warning: MongoDB connection failed - {e}")
    mongo_client = None


# ============================================================
# SQL MODELS
# ============================================================

class Holiday(db.Model):
    """SQL Model for Holiday"""
    __tablename__ = 'holidays'
    
    holiday_id = db.Column(db.Integer, primary_key=True)
    holiday_name = db.Column(db.String(100), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'holiday_id': self.holiday_id,
            'holiday_name': self.holiday_name
        }


class WeatherCondition(db.Model):
    """SQL Model for Weather Condition"""
    __tablename__ = 'weather_conditions'
    
    weather_id = db.Column(db.Integer, primary_key=True)
    weather_main = db.Column(db.String(50), nullable=False)
    weather_description = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'weather_id': self.weather_id,
            'weather_main': self.weather_main,
            'weather_description': self.weather_description
        }


class TrafficRecord(db.Model):
    """SQL Model for Traffic Record"""
    __tablename__ = 'traffic_records'
    
    record_id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    temp = db.Column(db.Float)
    rain_1h = db.Column(db.Float)
    snow_1h = db.Column(db.Float)
    clouds_all = db.Column(db.Integer)
    traffic_volume = db.Column(db.Integer)
    holiday_id = db.Column(db.Integer, db.ForeignKey('holidays.holiday_id'), nullable=True)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather_conditions.weather_id'), nullable=False)
    
    # Relationships
    holiday = db.relationship('Holiday')
    weather = db.relationship('WeatherCondition')
    
    def to_dict(self):
        return {
            'record_id': self.record_id,
            'date_time': self.date_time.isoformat() if self.date_time else None,
            'temp': self.temp,
            'rain_1h': self.rain_1h,
            'snow_1h': self.snow_1h,
            'clouds_all': self.clouds_all,
            'traffic_volume': self.traffic_volume,
            'holiday_id': self.holiday_id,
            'weather_id': self.weather_id,
            'holiday_name': self.holiday.holiday_name if self.holiday else None,
            'weather_main': self.weather.weather_main if self.weather else None,
            'weather_description': self.weather.weather_description if self.weather else None
        }


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def format_datetime(dt_string):
    """Convert string to datetime object"""
    try:
        return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    except:
        return datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')


# ============================================================
# SQL ENDPOINTS - TRAFFIC RECORDS
# ============================================================

@app.route('/api/v1/sql/traffic', methods=['POST'])
def create_traffic_record_sql():
    """Create a new traffic record in SQL database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['date_time', 'traffic_volume', 'weather_id']):
            return jsonify({'error': 'Missing required fields: date_time, traffic_volume, weather_id'}), 400
        
        # Parse datetime
        date_time = format_datetime(data['date_time'])
        
        # Create new record
        new_record = TrafficRecord(
            date_time=date_time,
            temp=data.get('temp'),
            rain_1h=data.get('rain_1h'),
            snow_1h=data.get('snow_1h'),
            clouds_all=data.get('clouds_all'),
            traffic_volume=data.get('traffic_volume'),
            holiday_id=data.get('holiday_id'),
            weather_id=data.get('weather_id')
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Traffic record created successfully',
            'record': new_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/traffic', methods=['GET'])
def get_all_traffic_records_sql():
    """Get all traffic records from SQL database with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = TrafficRecord.query.paginate(page=page, per_page=per_page)
        records = [record.to_dict() for record in pagination.items]
        
        return jsonify({
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'data': records
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/traffic/<int:record_id>', methods=['GET'])
def get_traffic_record_sql(record_id):
    """Get a specific traffic record by ID"""
    try:
        record = TrafficRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify(record.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/traffic/<int:record_id>', methods=['PUT'])
def update_traffic_record_sql(record_id):
    """Update a specific traffic record"""
    try:
        record = TrafficRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'date_time' in data:
            record.date_time = format_datetime(data['date_time'])
        if 'temp' in data:
            record.temp = data['temp']
        if 'rain_1h' in data:
            record.rain_1h = data['rain_1h']
        if 'snow_1h' in data:
            record.snow_1h = data['snow_1h']
        if 'clouds_all' in data:
            record.clouds_all = data['clouds_all']
        if 'traffic_volume' in data:
            record.traffic_volume = data['traffic_volume']
        if 'holiday_id' in data:
            record.holiday_id = data['holiday_id']
        if 'weather_id' in data:
            record.weather_id = data['weather_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Traffic record updated successfully',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/traffic/<int:record_id>', methods=['DELETE'])
def delete_traffic_record_sql(record_id):
    """Delete a specific traffic record"""
    try:
        record = TrafficRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message': 'Traffic record deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================
# SQL TIME-SERIES ENDPOINTS
# ============================================================

@app.route('/api/v1/sql/traffic/latest', methods=['GET'])
def get_latest_traffic_record_sql():
    """Get the latest (most recent) traffic record"""
    try:
        record = TrafficRecord.query.order_by(TrafficRecord.date_time.desc()).first()
        
        if not record:
            return jsonify({'error': 'No records found'}), 404
        
        return jsonify({
            'message': 'Latest traffic record',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/traffic/date-range', methods=['GET'])
def get_traffic_by_date_range_sql():
    """Get traffic records within a specified date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing required parameters: start_date, end_date'}), 400
        
        start_dt = format_datetime(start_date)
        end_dt = format_datetime(end_date)
        
        records = TrafficRecord.query.filter(
            TrafficRecord.date_time >= start_dt,
            TrafficRecord.date_time <= end_dt
        ).order_by(TrafficRecord.date_time).all()
        
        if not records:
            return jsonify({'error': 'No records found for the specified date range'}), 404
        
        return jsonify({
            'start_date': start_date,
            'end_date': end_date,
            'record_count': len(records),
            'records': [record.to_dict() for record in records]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# SQL HOLIDAY ENDPOINTS (CRUD)
# ============================================================

@app.route('/api/v1/sql/holidays', methods=['POST'])
def create_holiday_sql():
    """Create a new holiday"""
    try:
        data = request.get_json()
        
        if 'holiday_name' not in data:
            return jsonify({'error': 'Missing required field: holiday_name'}), 400
        
        new_holiday = Holiday(holiday_name=data['holiday_name'])
        db.session.add(new_holiday)
        db.session.commit()
        
        return jsonify({
            'message': 'Holiday created successfully',
            'holiday': new_holiday.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/holidays', methods=['GET'])
def get_all_holidays_sql():
    """Get all holidays"""
    try:
        holidays = Holiday.query.all()
        return jsonify([h.to_dict() for h in holidays]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/holidays/<int:holiday_id>', methods=['PUT'])
def update_holiday_sql(holiday_id):
    """Update a holiday"""
    try:
        holiday = Holiday.query.get(holiday_id)
        
        if not holiday:
            return jsonify({'error': 'Holiday not found'}), 404
        
        data = request.get_json()
        if 'holiday_name' in data:
            holiday.holiday_name = data['holiday_name']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Holiday updated successfully',
            'holiday': holiday.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/sql/holidays/<int:holiday_id>', methods=['DELETE'])
def delete_holiday_sql(holiday_id):
    """Delete a holiday"""
    try:
        holiday = Holiday.query.get(holiday_id)
        
        if not holiday:
            return jsonify({'error': 'Holiday not found'}), 404
        
        db.session.delete(holiday)
        db.session.commit()
        
        return jsonify({'message': 'Holiday deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================
# MONGODB ENDPOINTS - TRAFFIC RECORDS
# ============================================================

@app.route('/api/v1/mongodb/traffic', methods=['POST'])
def create_traffic_record_mongo():
    """Create a new traffic record in MongoDB"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['date_time', 'traffic_volume', 'weather']):
            return jsonify({'error': 'Missing required fields: date_time, traffic_volume, weather'}), 400
        
        # Prepare document
        document = {
            'date_time': datetime.fromisoformat(data['date_time'].replace('Z', '+00:00')),
            'traffic_volume': int(data['traffic_volume']),
            'weather': {
                'main': data['weather'].get('main'),
                'description': data['weather'].get('description'),
                'temp': float(data['weather'].get('temp', 0)),
                'rain_1h': float(data['weather'].get('rain_1h', 0)),
                'snow_1h': float(data['weather'].get('snow_1h', 0)),
                'clouds_all': int(data['weather'].get('clouds_all', 0))
            },
            'holiday': data.get('holiday')
        }
        
        result = traffic_collection.insert_one(document)
        
        return jsonify({
            'message': 'Traffic record created successfully',
            'id': str(result.inserted_id),
            'record': {
                **{k: v if k != 'date_time' else v.isoformat() for k, v in document.items()}
            }
        }), 201
        
    except PyMongoError as e:
        return jsonify({'error': f'MongoDB error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/mongodb/traffic', methods=['GET'])
def get_all_traffic_records_mongo():
    """Get all traffic records from MongoDB with pagination"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        skip = (page - 1) * per_page
        
        total = traffic_collection.count_documents({})
        records = list(
            traffic_collection.find({}, {'_id': 0}).skip(skip).limit(per_page).sort('date_time', -1)
        )
        
        # Convert datetime objects to ISO format
        for record in records:
            if 'date_time' in record:
                record['date_time'] = record['date_time'].isoformat()
        
        return jsonify({
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'data': records
        }), 200
        
    except PyMongoError as e:
        return jsonify({'error': f'MongoDB error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/mongodb/traffic/<record_id>', methods=['GET'])
def get_traffic_record_mongo(record_id):
    """Get a specific traffic record by ID"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        from bson import ObjectId
        
        record = traffic_collection.find_one({'_id': ObjectId(record_id)}, {'_id': 0})
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        if 'date_time' in record:
            record['date_time'] = record['date_time'].isoformat()
        
        return jsonify(record), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/mongodb/traffic/<record_id>', methods=['PUT'])
def update_traffic_record_mongo(record_id):
    """Update a specific traffic record"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        from bson import ObjectId
        
        data = request.get_json()
        
        # Prepare update document
        update_doc = {}
        if 'date_time' in data:
            update_doc['date_time'] = datetime.fromisoformat(data['date_time'].replace('Z', '+00:00'))
        if 'traffic_volume' in data:
            update_doc['traffic_volume'] = int(data['traffic_volume'])
        if 'weather' in data:
            update_doc['weather'] = {
                'main': data['weather'].get('main'),
                'description': data['weather'].get('description'),
                'temp': float(data['weather'].get('temp', 0)),
                'rain_1h': float(data['weather'].get('rain_1h', 0)),
                'snow_1h': float(data['weather'].get('snow_1h', 0)),
                'clouds_all': int(data['weather'].get('clouds_all', 0))
            }
        if 'holiday' in data:
            update_doc['holiday'] = data['holiday']
        
        result = traffic_collection.update_one(
            {'_id': ObjectId(record_id)},
            {'$set': update_doc}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Record not found'}), 404
        
        updated_record = traffic_collection.find_one({'_id': ObjectId(record_id)}, {'_id': 0})
        if 'date_time' in updated_record:
            updated_record['date_time'] = updated_record['date_time'].isoformat()
        
        return jsonify({
            'message': 'Traffic record updated successfully',
            'record': updated_record
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/mongodb/traffic/<record_id>', methods=['DELETE'])
def delete_traffic_record_mongo(record_id):
    """Delete a specific traffic record"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        from bson import ObjectId
        
        result = traffic_collection.delete_one({'_id': ObjectId(record_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify({'message': 'Traffic record deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# MONGODB TIME-SERIES ENDPOINTS
# ============================================================

@app.route('/api/v1/mongodb/traffic/latest', methods=['GET'])
def get_latest_traffic_record_mongo():
    """Get the latest (most recent) traffic record"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        record = traffic_collection.find_one({}, {'_id': 0}, sort=[('date_time', -1)])
        
        if not record:
            return jsonify({'error': 'No records found'}), 404
        
        if 'date_time' in record:
            record['date_time'] = record['date_time'].isoformat()
        
        return jsonify({
            'message': 'Latest traffic record',
            'record': record
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/mongodb/traffic/date-range', methods=['GET'])
def get_traffic_by_date_range_mongo():
    """Get traffic records within a specified date range"""
    try:
        if not mongo_client:
            return jsonify({'error': 'MongoDB connection not available'}), 500
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing required parameters: start_date, end_date'}), 400
        
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        records = list(
            traffic_collection.find(
                {
                    'date_time': {
                        '$gte': start_dt,
                        '$lte': end_dt
                    }
                },
                {'_id': 0}
            ).sort('date_time', 1)
        )
        
        if not records:
            return jsonify({'error': 'No records found for the specified date range'}), 404
        
        # Convert datetime objects to ISO format
        for record in records:
            if 'date_time' in record:
                record['date_time'] = record['date_time'].isoformat()
        
        return jsonify({
            'start_date': start_date,
            'end_date': end_date,
            'record_count': len(records),
            'records': records
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# HEALTH CHECK & ROOT ENDPOINTS
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'api': 'running',
            'sql': 'connected' if db.engine.execute('SELECT 1') else 'error',
            'mongodb': 'connected' if mongo_client else 'disconnected'
        }
    }
    return jsonify(status), 200


@app.route('/api/v1', methods=['GET'])
def api_info():
    """API information and available endpoints"""
    return jsonify({
        'name': 'Traffic Volume Time-Series API',
        'version': '1.0.0',
        'description': 'CRUD and time-series query endpoints for traffic data',
        'endpoints': {
            'sql': {
                'traffic': {
                    'POST /api/v1/sql/traffic': 'Create new record',
                    'GET /api/v1/sql/traffic': 'Get all records (paginated)',
                    'GET /api/v1/sql/traffic/<id>': 'Get specific record',
                    'PUT /api/v1/sql/traffic/<id>': 'Update record',
                    'DELETE /api/v1/sql/traffic/<id>': 'Delete record',
                    'GET /api/v1/sql/traffic/latest': 'Get latest record',
                    'GET /api/v1/sql/traffic/date-range?start_date=...&end_date=...': 'Get records by date range'
                },
                'holidays': {
                    'POST /api/v1/sql/holidays': 'Create holiday',
                    'GET /api/v1/sql/holidays': 'Get all holidays',
                    'PUT /api/v1/sql/holidays/<id>': 'Update holiday',
                    'DELETE /api/v1/sql/holidays/<id>': 'Delete holiday'
                }
            },
            'mongodb': {
                'traffic': {
                    'POST /api/v1/mongodb/traffic': 'Create new record',
                    'GET /api/v1/mongodb/traffic': 'Get all records (paginated)',
                    'GET /api/v1/mongodb/traffic/<id>': 'Get specific record',
                    'PUT /api/v1/mongodb/traffic/<id>': 'Update record',
                    'DELETE /api/v1/mongodb/traffic/<id>': 'Delete record',
                    'GET /api/v1/mongodb/traffic/latest': 'Get latest record',
                    'GET /api/v1/mongodb/traffic/date-range?start_date=...&end_date=...': 'Get records by date range'
                }
            }
        }
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to Traffic Volume API',
        'docs': 'See /api/v1 for endpoint documentation'
    }), 200


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================
# APP INITIALIZATION
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Warning: Could not create tables - {e}")
    
    print("=" * 60)
    print("Traffic Volume API Server Starting...")
    print("=" * 60)
    print("\nAvailable Endpoints:")
    print("  - API Info: http://localhost:5000/api/v1")
    print("  - Health Check: http://localhost:5000/api/health")
    print("\nSQL Endpoints: /api/v1/sql/...")
    print("MongoDB Endpoints: /api/v1/mongodb/...")
    print("\n" + "=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

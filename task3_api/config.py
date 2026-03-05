"""
Configuration settings for the Traffic API
"""
import os
from datetime import datetime

class Config:
    """Base configuration"""
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', True)
    
    # SQL Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/traffic_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MongoDB
    MONGO_URI = os.getenv(
        'MONGO_URI',
        'mongodb://localhost:27017/traffic_db'
    )
    
    # API Settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Export appropriate config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

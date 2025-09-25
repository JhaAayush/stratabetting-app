"""
Configuration settings for Stratabetting application
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///stratabetting.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Betting settings
    INITIAL_BALANCE = 200
    MIN_BET_AMOUNT = 1
    MAX_BET_AMOUNT = 1000
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Pagination settings
    POSTS_PER_PAGE = 20
    EVENTS_PER_PAGE = 10
    
    # Email settings (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Application settings
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@stratabetting.com'
    APP_NAME = 'Stratabetting - Kritansh 2024'
    
    # Team settings
    TEAMS = [
        'Alpha Wolves',
        'Black Pirates', 
        'Dragon Slayers',
        'Viking Warriors'
    ]
    
    # Sports settings
    SPORTS = [
        'Cricket',
        'Football',
        'Basketball',
        'Chess',
        'Futsal',
        'Table Tennis',
        'Carrom',
        'FIFA',
        'BGMI',
        'Badminton',
        'Pool',
        'Tug of War',
        'Athletics',
        'Frisbee'
    ]
    
    # Event types
    EVENT_TYPES = [
        'Match',
        'Semi-Final',
        'Final',
        'Qualifier',
        'League'
    ]
    
    # Question types
    QUESTION_TYPES = [
        'team_winner',
        'total_runs',
        'total_sixes',
        'final_teams',
        'score_prediction',
        'other'
    ]

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

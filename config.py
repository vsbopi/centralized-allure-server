#!/usr/bin/env python3
"""
Configuration file for the Centralized Allure Reports Server
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # S3 Configuration
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.S3_BUCKET_NAME:
            raise ValueError("S3_BUCKET_NAME environment variable is required")
        
        return True

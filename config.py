import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    MODEL_PATH = os.getenv("MODEL_PATH_PRODUCTION")                
    DESIRED_TIMEZONE = os.getenv("DESIRED_TIMEZONE_PRODUCTION")       
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH_PRODUCTION") 
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_PRODUCTION")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    MODEL_PATH = os.getenv("MODEL_PATH_TESTING")                
    DESIRED_TIMEZONE = os.getenv("DESIRED_TIMEZONE_TESTING")       
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH_TESTING")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_TESTING")  

class DevelopmentConfig(Config):
    DEVELOPMENT=True
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    MODEL_PATH = os.getenv("MODEL_PATH_DEVELOPMENT")                
    DESIRED_TIMEZONE = os.getenv("DESIRED_TIMEZONE_DEVELOPMENT")       
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH_DEVELOPMENT")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_DEVELOPMENT")  
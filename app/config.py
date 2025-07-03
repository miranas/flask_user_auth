import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # General settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    #DATABASE_URL = os.getenv("DATABASE_URL")
    #DEBUG = False
    #TESTING = False
    


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "Development"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"
    
class ProductionConfig(Config):
    #Debug is inherited from Config class an os set to False
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False















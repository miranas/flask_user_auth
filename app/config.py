import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # General settings    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "Development"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI","sqlite:///dev.db")
    
     
class ProductionConfig(Config):
    #Debug is inherited from Config class an os set to False
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI","sqlite:///prod.db")















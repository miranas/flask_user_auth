from flask import Flask
import os
from dotenv import load_dotenv
from .config import DevelopmentConfig, ProductionConfig
from .routes.auth_routes_api import auth_bp
from .routes.routes import main
from .database import db
from flask_mail import Mail
from .import logging_config


#Initialize Flask_Mail instance at global scope
mail = Mail()

#load environment variables from .env file
load_dotenv()


#the app factory
def create_app():  

    app = Flask(__name__)
    
    #get the environment variable to determine the configuration
    env = os.environ.get("FLASK_ENV", "production")

    #set the configuration based on the environment
    if env == "development":
        
        app.config.from_object(DevelopmentConfig)

    else:
        
        app.config.from_object(ProductionConfig)

    
    
    
    #initialize and bind SQLAlchemy extension to the app to set db connections
    db.init_app(app) 
   
        
    #initialize Flask-Mail extension
    mail.init_app(app)


    #create context from model imported as well as db instance 
    with app.app_context():
        db.create_all()

        #Let's register Blueprint instances all in one place
        app.register_blueprint(auth_bp, url_prefix = "/auth")
        #app.register_blueprint(main)
        

    return app   


   
    
    
   

   


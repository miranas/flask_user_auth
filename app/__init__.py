from flask import Flask
import os
from dotenv import load_dotenv
from .config import DevelopmentConfig, ProductionConfig
from .routes.auth_routes_api import auth_bp
from .routes.routes import main
from .database import db
from flask_mail import Mail
#from .import logging_config
import sentry_sdk


# Initialize Flask_Mail instance at global scope
mail = Mail()

# load environment variables from .env file
load_dotenv()


# the app factory
def create_app():

    app = Flask(__name__)

    sentry_sdk.init(
        dsn="https://6481ea9d0ea1b61ae5724ba8ca5ba630@o4504918162538496.ingest.us.sentry.io/4509668672077824",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )

    # get the environment variable to determine the configuration
    env = os.environ.get("FLASK_ENV", "production")

    # set the configuration based on the environment
    if env == "development":

        app.config.from_object(DevelopmentConfig)

    else:

        app.config.from_object(ProductionConfig)
    
    #Sets the secret key from environment variable if available, otherwise use whatewer in config or finaly sqlite:///test.db
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        app.config.get("SQLALCHEMY_DATABASE_URI", "sqlite:///test.db")  # type: ignore
    )

    # initialize and bind SQLAlchemy extension to the app to set db connections
    db.init_app(app)

    # initialize Flask-Mail extension
    mail.init_app(app)

    # create context from model imported as well as db instance
    with app.app_context():
        db.create_all()

        # Let's register Blueprint instances all in one place
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(main)  
         
    return app

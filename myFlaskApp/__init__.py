# Import the Flask class from the flask module. This class is the main entry point for any Flask web application.
from flask import Flask

# Import the Config class from the config module in the current package.
from .config import Config

# Import the SQLAlchemy instance and the init_db function from the db module in the current package.
from .db import db, init_db

# Import the configure_logging function from the logger module in the current package.
from .logger import configure_logging

import logging
from logging.handlers import RotatingFileHandler

def create_app(test_config=None):
    # Create an instance of the Flask class. The first argument is the name of the application’s module or package.
    # The instance_relative_config argument is set to True so configuration files are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration from the Config class.
    app.config.from_object(Config)

    # If a test configuration is provided, load it into the application's configuration.
    if test_config:
        app.config.from_mapping(test_config)

    with app.app_context():
        # Initialize the SQLAlchemy instance with the Flask application.
        init_db(app)

        # Import the FileRecord model from the models module in the current package.
        from .models import FileRecord

        # Import the blueprint from the auth module in the current package.
        from .auth import auth_bp
        
        # Register the blueprint with the Flask application.
        app.register_blueprint(auth_bp)

        # Set the log level of the logger to the lowest level you want to log
        app.logger.setLevel(logging.DEBUG)

        # Create a StreamHandler for logging to the console
        # Set its log level to INFO, so it only logs messages with level INFO and above
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        # Create a FileHandler for logging to a file
        # Set its log level to DEBUG, so it logs all messages
        file_handler = RotatingFileHandler('flask.log', maxBytes=1024*1024*100, backupCount=20)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        app.logger.addHandler(stream_handler)
        app.logger.addHandler(file_handler)

        # Configure logging for the Flask application.
        configure_logging(app)

        # Define logging statements
        app.logger.info('App initialized successfully')

    # Return the Flask application.
    return app

# Import the logging module to enable logging
import logging

# Import the RotatingFileHandler from the logging.handlers module. This handler rotates log files when they reach a certain size.
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    # Create a formatter for the log messages.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create a rotating file handler that writes to app.log, rotates the log file when it reaches 1MB, and keeps the last 5 log files.
    file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=5)
    
    # Set the log level of the file handler to INFO.
    file_handler.setLevel(logging.INFO)
    
    # Set the formatter of the file handler.
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the application's logger.
    app.logger.addHandler(file_handler)
    
    # Set the log level of the application's logger to INFO.
    app.logger.setLevel(logging.INFO)
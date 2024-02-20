# Import the os module to interact with the operating system
import os

# Define a Config class to hold configuration variables
class Config:
    # Define a secret key for the Flask application. This should be unique and secure in a production application.
    # We're using the os.getenv function to read the SECRET_KEY environment variable, with a default value of 'dev'.
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # Define the SQLAlchemy database URI. This should point to your database server.
    # We're using the os.getenv function to read the SQLALCHEMY_DATABASE_URI environment variable, with a default value.
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://pedro:azul@localhost/genome')
    
    # Disable SQLAlchemy's event system, which is not needed in most cases and consumes system resources.
    # We're using the os.getenv function to read the SQLALCHEMY_TRACK_MODIFICATIONS environment variable, with a default value of False.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    # Define the folder where uploaded files will be stored.
    # We're using the os.getenv function to read the UPLOAD_FOLDER environment variable, with a default value of 'uploads'.
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
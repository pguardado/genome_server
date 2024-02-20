# Import the SQLAlchemy class from the flask_sqlalchemy module. 
# SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) system for Python, 
# providing a full suite of well known enterprise-level persistence patterns.
# Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. 
from flask_sqlalchemy import SQLAlchemy

# Import the Migrate class from the flask_migrate module.
# Flask-Migrate is an extension for Flask that handles SQLAlchemy database migrations using Alembic.
from flask_migrate import Migrate

# Create an instance of the SQLAlchemy class. 
# This instance, often named `db`, will be used to interact with the database.
db = SQLAlchemy()

# Define a function to initialize the SQLAlchemy instance with a Flask application.
# This function is typically called in your application factory.
def init_db(app):
    # Call the init_app method on the SQLAlchemy instance, passing in the Flask application.
    # This sets up the SQLAlchemy instance to work with the Flask application.
    # It also configures a few defaults for us such as the database URI being pulled from the app configuration.
    db.init_app(app)

    # Create an instance of the Migrate class. 
    # This instance, often named `migrate`, will be used to handle database migrations.
    # It is initialized with the Flask application instance and the SQLAlchemy database instance.
    migrate = Migrate(app, db)
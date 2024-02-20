# Import the Blueprint class from the flask module.
from flask import Blueprint

# Create a new blueprint named 'main'. This blueprint will be used to organize your main routes.
main_bp = Blueprint('main', __name__)

# Define a route for the URL '/' (the home page of your application). 
# When a user visits this URL, Flask will call the index function.
@main_bp.route('/')
def index():
    # The index function returns the string 'Home Page'. 
    # This is what the user will see when they visit the home page of your application.
    return 'Home Page'
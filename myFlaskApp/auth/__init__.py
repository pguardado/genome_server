# myFlaskApp/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Import routes after Blueprint is fully defined
from .auth_routes import *
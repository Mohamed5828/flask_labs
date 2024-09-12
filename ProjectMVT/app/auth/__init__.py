from flask import Blueprint

auth_routes = Blueprint("auth", __name__, url_prefix="/auth", static_folder='static', template_folder='templates')
from app.auth.auth import *
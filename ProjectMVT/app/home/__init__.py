from flask import Blueprint

home_routes = Blueprint('home', __name__, url_prefix='', static_folder='static', template_folder='templates')
from app.home.home import *
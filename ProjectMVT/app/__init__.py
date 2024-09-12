from flask import Flask
from flask_migrate import Migrate
from .config import config_options
from .models import db

from .home import home_routes
from .books import books_routes
from .auth import auth_routes
from flask import render_template, url_for
import base64

def create_app(config_type='dev'):
    def b64encode_filter(image):
        return base64.b64encode(image).decode('utf-8')
    app = Flask(__name__)

    # Configure App
    current_config = config_options[config_type]
    print(current_config)
    app.config.from_object(current_config) # configure debug=True

    # @app.template_filter('b64encode')

    app.jinja_env.filters['b64encode'] = b64encode_filter

    # Configure Database
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = current_config.SQLALCHEMY_DATABASE_URI
    migrate = Migrate(app=app, db=db)

    # secret key 
    app.secret_key = 'MOHAMEDAHMED'

    # Create Tables
    with app.app_context(): # production
        db.create_all()

    # Register Blueprints
    app.register_blueprint(home_routes)
    app.register_blueprint(books_routes)
    app.register_blueprint(auth_routes)

    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template("error.html")
    
    return app

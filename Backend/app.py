# app.py
#from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory, url_for
#from wtforms import StringField, PasswordField, SubmitField
#from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
#from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from flask_mail import Mail
from flask_caching import Cache
from functools import wraps
from cache import cache
from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.sponsor_controller import sponsor_bp
from controllers.influencer_controller import influencer_bp
from db import db


# Initialize Flask app
application = Flask(__name__)

# CORS Configuration
CORS(application)
CORS(application, resources={r"/*": {"origins": "http://192.168.1.44:8080"}})

# Database Configuration
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'b65e69d8907c4b98a541c3e6eb2db78d'
application.config['WTF_CSRF_ENABLED'] = False

# Redis Cache Configuration
application.config['CACHE_TYPE'] = 'redis'
application.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
application.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Mail Configuration
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USERNAME'] = 'qstykks@gmail.com'  # Replace with your email
application.config['MAIL_PASSWORD'] = 'bjvz exbd lmed surz'    # Replace with your app password

# Initialize extensions
db.init_app(application)
jwt = JWTManager(application)
migrate = Migrate(application, db)
mail = Mail(application)
# mail.init_app(application)
# cache = Cache(app)
cache.init_app(application)

# Register blueprints
application.register_blueprint(auth_bp, url_prefix='/auth')
application.register_blueprint(admin_bp, url_prefix='/admin')
application.register_blueprint(sponsor_bp, url_prefix='/sponsor')
application.register_blueprint(influencer_bp, url_prefix='/influencer')

# Cache decorator for general use
def cached_response(timeout=5 * 60, key_prefix='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key_prefix % request.full_path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
    application.run(debug=True, port=5000)
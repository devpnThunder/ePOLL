"""Initial system launch configuration file"""
from flask import Flask
from .extensions import db, migrate, csrf, login_manager
from .config import App_Config
from flask_security import Security
# from models import *
from auth import *
from admin import *
from voter import *

#==================================================================#
# App Configuration
#==================================================================#
def create_app():
    """
    Application factory function that creates and configures the app
    """
    # Import Models
    form app.models import Role, User

    app = Flask(__name__)
    application = app

    # Initialize the Configuration file
    app.config.from_object(App_Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'


    # Register app Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(abp)
    app.register_blueprint(sbp)


    # Default route redirect to app login page
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))


    # Comma formater for larger numbers
    @app.template_filter('comma_format')
    def comma_format(value):
        if value is None:
            return "0"
        return "{:,.2f}".format(value)

    # Logged in user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register error handlers
    register_error_handlers(app)


    return app

#===End=of=App=Settings============================================#
"""Initial system launch configuration file"""
from flask import Flask
from .extensions import db, migrate, login_manager
from app.config import App_Config
from app.models import *
from app.auth import *
from app.admin import *
from app.voter import *
from app.settings import sbp
from app.dbsetup import setup_database
from app.errors import register_error_handlers

#==================================================================#
# App Configuration
#==================================================================#
def create_app():
    """
    Application factory function that creates and configures the app
    """
    # Import Models
    # from app.models import Role, User
    # from app.auth import auth
    # from app.admin import admin
    # from app.voter import voter

    app = Flask(__name__)
    application = app

    # Initialize the Configuration file
    app.config.from_object(App_Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    # Register app Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(abp)
    app.register_blueprint(vbp)
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

    # Setup database and create initial roles and users
    with app.app_context():
        setup_database(app)


    return app

#===End=of=App=Settings============================================#
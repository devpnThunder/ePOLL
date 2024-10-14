import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Extensions Initialization
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
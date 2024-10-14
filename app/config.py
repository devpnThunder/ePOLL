"""Config file that stores secret keys and db connections."""
import os

class App_Config:
    """
    App Configurations
    """

    # Core Flask Configuration
    SECRET_KEY = os.urandom(32)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # DEBUG = True

    # Database Connection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'ePOLL.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///testerApp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
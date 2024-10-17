"""Admin configuration file that contains admin views and routes."""
from app.models import *
from app.forms import *
from app.auth import role_required
from flask import (Blueprint, Flask, flash, redirect, render_template, request, url_for, send_file)
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.sql import func, or_
from datetime import datetime
import math
from io import BytesIO

abp = Blueprint('admin', __name__, url_prefix='/admin')

#===================================================================================================#
# Admin View routes
# Contains all the routes and pages for Admin View Pages
#===================================================================================================#

@abp.route('/dashboard/')
# @login_required
# @role_required('Super', 'Admin')
def dashboard():
    """
    Admin Dashboard Page
    """
    return render_template('admin/dashboard.html', title='Dashboard', DASHBOARD=True)

@abp.route('/settings/')
# @login_required
# @role_required('Super', 'Admin')
def settings():
    """
    Settings landing Page
    """
    return render_template('admin/settings/index.html', title='Settings', SETTINGS=True)



#===End=of=Admin=routes=============================================================================#
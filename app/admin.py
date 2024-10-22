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
@login_required
@role_required('Super', 'Admin')
def dashboard():
    """
    Admin Dashboard Page
    """
    count_voters = Voter.query.count()
    count_category = Category.query.count()
    count_motions = Motion.query.count()
    count_agendas = Agenda.query.count()
    return render_template('admin/dashboard.html', title='Dashboard', 
                           count_voters=count_voters,
                           count_category=count_category,
                           count_motions=count_motions,
                           count_agendas=count_agendas,
                           DASHBOARD=True)


@abp.route('/voters/', methods=["GET", "POST"])
@login_required
@role_required('Super', 'Admin')
def voters():
    """
    available voters
    """
    count_voters = Voter.query.count()
    search = request.args.get('search', '') # Search query from input box
    sort_by = request.args.get('sort_by', 'date_registered')  # Default sorting by date_registered
    sort_order = request.args.get('sort_order', 'asc')  # Default sorting order is ascending
    query = Voter.query

    # searching
    if search:
        query = query.join(Constituency).filter(
            (Voter.fullname.ilike(f'%{search}%')) |
            (Voter.id_number.ilike(f'%{search}%')) |
            (Voter.email.ilike(f'%{search}%')) |
            (Constituency.name.ilike(f'%{search}%')))

    # sorting
    if sort_order == 'asc':
        query = query.order_by(getattr(Voter, sort_by).asc())
    else:
        query = query.order_by(getattr(Voter, sort_by).desc())

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 15
    votersList = query.order_by(Voter.date_registered.desc()).paginate(page=page, per_page=page_size)

    if not votersList.items:  # `items` returns the records on the current page
        flash('No voter records added yet!', 'info')

    return render_template('admin/voter/list.html', title='Voters', 
                           count_voters=count_voters, votersList=votersList, 
                           sort_by=sort_by, sort_order=sort_order, page_size=page_size, VOTERS=True)


#===End=of=Admin=routes=============================================================================#
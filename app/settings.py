"""Admin configuration file that contains admin views and routes."""
from app.models import *
from app.forms import *
from app.auth import role_required
from flask import (Blueprint, Flask, flash, redirect, render_template, request, url_for, send_file)
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.sql import func, or_
from datetime import datetime
from sqlalchemy.orm import joinedload
import math
from io import BytesIO

sbp = Blueprint('settings', __name__, url_prefix='/settings')

#===================================================================================================#
# Admin View routes
# Contains all the routes and pages for Admin View Pages
#===================================================================================================#
@sbp.route('/index/')
# @login_required
# @role_required('Super', 'Admin')
def index():
    """
    Settings landing Page
    """
    count_category = Category.query.count()
    count_county = County.query.count()
    count_constituency = Constituency.query.count()
    count_users = User.query.count()
    count_roles = Role.query.count()
    return render_template('admin/settings/index.html', title='Settings', 
                           count_category=count_category, count_county=count_county,
                           count_constituency=count_constituency,
                           count_users=count_users, count_roles=count_roles,
                           SETTINGS=True)


#=================================================================#
# Role routes section starts Here
# Contains all Role routes and any associated routes
#=================================================================#
@sbp.route('/roles/')
# @login_required
# @role_required('Super', 'Admin')
def roles():
    """
    Load System Roles
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    system_roles = Role.query.order_by(Role.created_at.desc()).paginate(page=page, per_page=page_size)
    if not system_roles:
        flash('No Role records added Yet!', 'warning')

    return render_template('admin/settings/role/list.html', title='Roles', system_roles=system_roles, SETTINGS=True)


@sbp.route('/new_role/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_role():
    """
    Create New Role
    """
    form = RoleForm()
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        permissions = form.permissions.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newrole = Role(name=name, description=description)
                db.session.add(newrole)
                db.session.commit()

                for permission in permissions:
                    role_permissions = RolePermission(role_id=newrole.id, permission_id=permission)
                    db.session.add(role_permissions)
                    db.session.commit()

                flash(f'{name} role is created successfully!', 'success')
                return redirect(url_for('settings.roles'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('settings.roles'))
            
    return render_template('admin/settings/role/create.html', title='New Role', form=form, SETTINGS=True)


@sbp.route('/edit_role/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_role(id):
    """
    Edit Role View or 404 if not found
    """
    selected_role = Role.query.get_or_404(id)
    form = RoleForm(obj=selected_role)
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]

    if request.method == 'GET':
        form.permissions.data = [p.id for p in selected_role.permissions]

    if form.validate_on_submit():
        selected_role.name = form.name.data
        selected_role.description = form.description.data

        selected_permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        selected_role.permissions = selected_permissions
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(f'{selected_role.name} role is updated Successfully!', 'success')
                return redirect(url_for('settings.roles'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('settings.roles'))

    return render_template('admin/settings/role/edit.html', title='Edit Role', form=form, SETTINGS=True)


@sbp.route('/delete_role/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_role(id):
    """
    Delete Role View or 404 if not found.
    """
    selected_role = Role.query.get_or_404(id)
    form = RoleForm(obj=selected_role)
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]

    if selected_role == 'Super':
        flash('The "Super" role cannot be deleted!', 'danger')
        return redirect(url_for('settings.roles'))

    if form.validate_on_submit():
        try:
            db.session.delete(selected_role)
            db.session.commit()
            flash('Role is deleted successfully!', 'success')
            return redirect(url_for('settings.roles'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('settings.roles'))

        
    return render_template('admin/settings/role/delete.html', title='Delete Role', form=form, SETTINGS=True)
#===End=of=Roles=routes===========================================#



#=================================================================#
# User routes section starts Here
# Contains all User routes and any associated routes
#=================================================================#
@sbp.route('/users/')
# @login_required
# @role_required('Super', 'Admin')
def users():
    """
    Load System Users
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    system_users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=page_size)
    if not system_users:
        flash('No User records added Yet!', 'warning')

    return render_template('admin/settings/user/list.html', title='Users', system_users=system_users, SETTINGS=True)


@sbp.route('/new_user/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_user():
    """
    Create New User
    """
    form = UserForm()
    form.roles.choices = [(r.id, r.name) for r in Role.query.filter(Role.name != 'Super').all()]

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        roles = form.roles.data

        error = None

        test = User.query.filter_by(email=email).first()

        if error:
            flash(error)
        else:
            if test:
                flash(f'{email} already exists!', 'warning')
                return redirect(url_for('settings.users'))
            else:
                try:
                    newuser = User(email=email, created_at=datetime.now())
                    newuser.set_password(password)
                    db.session.add(newuser)
                    db.session.commit()

                    userrole = UserRole(user_id=newuser.id, role_id=roles)
                    db.session.add(userrole)
                    db.session.commit()

                    flash(f'Account for {email} is created successfully!', 'success')
                    return redirect(url_for('settings.users'))
                except Exception as e:
                    flash(f'There was an error saving data: {e}!', 'danger')
                    db.session.rollback
                    return redirect(url_for('settings.users'))
            
    return render_template('admin/settings/user/create.html', title='New User', form=form, SETTINGS=True)


@sbp.route('/edit_user/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_user(id):
    """
    Edit User View or 404 if not found
    """
    selected_user = User.query.get_or_404(id)
    form = UserForm(obj=selected_user)
    form.roles.choices = [(r.id, r.name) for r in Role.query.filter(Role.name != 'Super').all()]

    if request.method == 'GET':
        form.roles.data = [r.id for r in selected_user.roles]

    if form.validate_on_submit():
        selected_user.email = form.email.data
        selected_user.password = form.password.data

        selected_roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
        selected_user.roles = selected_roles

        error = None

        if error:
            flash(error)
        else:
            try:
                UserRole(user_id=selected_user.id, role_id=form.roles.data)
                db.session.commit()
                flash(f'{selected_user.email} is updated Successfully!', 'success')
                return redirect(url_for('settings.users'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('settings.users'))
            
    form.email.data = selected_user.email
    form.roles.data = [role.id for role in selected_user.roles]

    return render_template('admin/settings/user/edit.html', title='Edit User', form=form, SETTINGS=True)


@sbp.route('/delete_user/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_user(id):
    """
    Delete User View or 404 if not found.
    """
    selected_user = User.query.get_or_404(id)
    form = UserForm(obj=selected_user)
    # form.roles.choices = [(r.id, r.name) for r in Role.query.all()]

    if selected_user.email == 'superadmin@mail.com':
        flash('The Super User cannot be deleted!', 'danger')
        return redirect(url_for('settings.users'))

    if form.validate_on_submit():
        try:
            db.session.delete(selected_user)
            db.session.commit()
            flash('User is deleted successfully!', 'success')
            return redirect(url_for('settings.users'))
        except Exception as e:
            flash(f'There was an error during the deletion: {str(e)}!', 'danger')
            db.session.rollback()
            return redirect(url_for('settings.users'))

        
    return render_template('admin/settings/user/delete.html', title='Delete User', form=form, SETTINGS=True)
#===End=of=User=routes============================================#



#=================================================================#
# County routes section starts Here
# Contains all County routes and any associated routes
#=================================================================#
@sbp.route('/counties/')
# @login_required
# @role_required('Super', 'Admin')
def counties():
    """
    Load all available counties
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    all_counties = County.query.order_by(County.created_at.desc()).paginate(page=page, per_page=page_size)
    if not all_counties:
        flash('No County records added Yet!', 'warning')

    return render_template('admin/settings/county/list.html', 
                           title='Counties', all_counties=all_counties, SETTINGS=True)


@sbp.route('/new_county/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_county():
    """
    Create New County
    """
    form = CountyForm()

    if form.validate_on_submit():
        name = form.name.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newcounty = County(name=name, created_at=datetime.now())
                db.session.add(newcounty)
                db.session.commit()

                flash(f'{name} county is created successfully!', 'success')
                return redirect(url_for('settings.counties'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('settings.counties'))
            
    return render_template('admin/settings/county/create.html', title='New County', form=form, SETTINGS=True)


@sbp.route('/edit_county/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_county(id):
    """
    Edit County View or 404 if not found
    """
    selected_county = County.query.get_or_404(id)
    form = CountyForm(obj=selected_county)

    if form.validate_on_submit():
        selected_county.name = form.name.data
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(f'{selected_county.name} county is updated Successfully!', 'success')
                return redirect(url_for('settings.counties'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('settings.counties'))

    return render_template('admin/settings/county/edit.html', title='Edit County', form=form, SETTINGS=True)


@sbp.route('/delete_county/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_county(id):
    """
    Delete County View or 404 if not found.
    """
    selected_county = County.query.get_or_404(id)
    form = CountyForm(obj=selected_county)

    if form.validate_on_submit():
        try:
            db.session.delete(selected_county)
            db.session.commit()
            flash('County is deleted successfully!', 'success')
            return redirect(url_for('settings.counties'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('settings.counties'))

        
    return render_template('admin/settings/county/delete.html', title='Delete County', form=form, SETTINGS=True)
#===End=of=Counties=routes===========================================#



#=================================================================#
# Constituency routes section starts Here
# Contains all Constituency routes and any associated routes
#=================================================================#
@sbp.route('/constituencies/')
# @login_required
# @role_required('Super', 'Admin')
def constituencies():
    """
    Load all available constituencies
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    all_constituencies = Constituency.query.order_by(Constituency.created_at.desc()).paginate(page=page, per_page=page_size)
    if not all_constituencies:
        flash('No Role records added Yet!', 'warning')

    return render_template('admin/settings/constituency/list.html', 
                           title='Constituencies', all_constituencies=all_constituencies, SETTINGS=True)


@sbp.route('/new_constituency/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_constituency():
    """
    Create New Constituency
    """
    form = ConstituencyForm()
    form.county_id.choices = [(c.id, c.name) for c in County.query.all()]

    if form.validate_on_submit():
        county_id = form.county_id.data
        name = form.name.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newconstituency = Constituency(county_id=county_id, name=name, created_at=datetime.now())
                db.session.add(newconstituency)
                db.session.commit()

                flash(f'{name} constituency is created successfully!', 'success')
                return redirect(url_for('settings.constituencies'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('settings.constituencies'))
            
    return render_template('admin/settings/constituency/create.html', title='New Constituency', form=form, SETTINGS=True)


@sbp.route('/edit_constituency/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_constituency(id):
    """
    Edit Constituency View or 404 if not found
    """
    selected_constituency = Constituency.query.get_or_404(id)
    form = ConstituencyForm(obj=selected_constituency)
    form.county_id.choices = [(c.id, c.name) for c in County.query.all()]

    if form.validate_on_submit():
        selected_constituency.county_id = form.county_id.data
        selected_constituency.name = form.name.data
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(f'{selected_constituency.name} constituency is updated Successfully!', 'success')
                return redirect(url_for('settings.constituencies'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('settings.constituencies'))

    return render_template('admin/settings/constituency/edit.html', title='Edit Constituency', form=form, SETTINGS=True)


@sbp.route('/delete_constituency/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_constituency(id):
    """
    Delete Constituency View or 404 if not found.
    """
    selected_constituency = Constituency.query.get_or_404(id)
    form = ConstituencyForm(obj=selected_constituency)
    form.county_id.choices = [(c.id, c.name) for c in County.query.all()]

    if form.validate_on_submit():
        try:
            db.session.delete(selected_constituency)
            db.session.commit()
            flash('Constituency is deleted successfully!', 'success')
            return redirect(url_for('settings.constituencies'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('settings.constituencies'))

        
    return render_template('admin/settings/constituency/delete.html', title='Delete Constituency', form=form, SETTINGS=True)
#===End=of=Constituency=routes=====================================#



#=================================================================#
# Category routes section starts Here
# Contains all Category routes and any associated routes
#=================================================================#
@sbp.route('/categories/')
# @login_required
# @role_required('Super', 'Admin')
def categories():
    """
    Load all available categories
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    all_categories = Category.query.order_by(Category.created_at.desc()).paginate(page=page, per_page=page_size)
    if not all_categories:
        flash('No Category records added Yet!', 'warning')

    return render_template('admin/settings/category/list.html', 
                           title='Categories', all_categories=all_categories, SETTINGS=True)


@sbp.route('/new_category/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_category():
    """
    Create New Category
    """
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newcategory = Category(name=name, created_at=datetime.now())
                db.session.add(newcategory)
                db.session.commit()

                flash(f'{name} category is created successfully!', 'success')
                return redirect(url_for('settings.categories'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('settings.categories'))
            
    return render_template('admin/settings/category/create.html', title='New Category', form=form, SETTINGS=True)


@sbp.route('/edit_category/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_category(id):
    """
    Edit Category View or 404 if not found
    """
    selected_category = Category.query.get_or_404(id)
    form = CategoryForm(obj=selected_category)

    if form.validate_on_submit():
        selected_category.name = form.name.data
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(f'{selected_category.name} category is updated Successfully!', 'success')
                return redirect(url_for('settings.categories'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('settings.categories'))

    return render_template('admin/settings/category/edit.html', title='Edit Category', form=form, SETTINGS=True)


@sbp.route('/delete_category/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_category(id):
    """
    Delete Category View or 404 if not found.
    """
    selected_category = Category.query.get_or_404(id)
    form = CategoryForm(obj=selected_category)

    if form.validate_on_submit():
        try:
            db.session.delete(selected_category)
            db.session.commit()
            flash('Category is deleted successfully!', 'success')
            return redirect(url_for('settings.categories'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('settings.categories'))

        
    return render_template('admin/settings/category/delete.html', title='Delete Category', form=form, SETTINGS=True)
#===End=of=Category=routes===========================================#



#===End=of=Admin=routes=============================================================================#
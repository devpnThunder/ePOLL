"""Authentication configuration file that contains auth views and routes."""
import functools
from app.models import *
from app.forms import *
from flask import (Blueprint, flash, g, redirect, render_template, session, url_for, abort)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .extensions import login_manager
from datetime import datetime
from functools import wraps
from sqlalchemy import or_

# login_manager = LoginManager()
auth = Blueprint('auth', __name__, url_prefix='/auth')


#=================================================================#
# Authorization routes section starts Here
# Contains all Authorization routes and any associated routes
#=================================================================#
@auth.route('/register/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def register():
    """
    New Voter Registration
    """
    form = RegistrationForm()
    form.constituency_id.choices = [(c.id, c.name) for c in Constituency.query.all()]
    form.roles.choices = [(r.id, r.name) for r in Role.query.filter(Role.name == 'Voter').all()]

    if form.validate_on_submit():
        constituency_id = form.constituency_id.data
        surname = form.surname.data
        firstname = form.firstname.data
        othername = form.othername.data
        fullname = (firstname + ' ' + othername + ' ' + surname )
        gender = form.gender.data
        id_number = form.id_number.data
        email = form.email.data
        password = form.password.data
        roles = form.roles.data

        error = None

        test = Voter.query.filter(or_(Voter.email == email, Voter.id_number == id_number)).first()

        if error:
            flash(error)
        else:
            if test:
                flash(f'{email} already exists!', 'warning')
                return redirect(url_for('auth.register'))
            else:
                try:
                    newuser = User(email=email, created_at=datetime.now())
                    newuser.set_password(password)
                    db.session.add(newuser)
                    db.session.commit()

                    userrole = UserRole(user_id=newuser.id, role_id=roles)
                    db.session.add(userrole)
                    db.session.commit()

                    newvoter = Voter(user_id=newuser.id, constituency_id=constituency_id, 
                                    surname=surname, firstname=firstname, othername=othername,
                                    fullname=fullname, gender=gender, id_number=id_number,
                                    email=email, date_registered=datetime.now())
                    db.session.add(newvoter)
                    db.session.commit()

                    flash(f'Account for {(firstname + ' ' + surname)}  is created successfully!', 'success')
                    return redirect(url_for('auth.login'))
                except Exception as e:
                    flash(f'There was an error saving data: {e}!', 'danger')
                    db.session.rollback
                    return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html', title='New Voter Registration', form=form)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)



#
# This is the Login Route. It returns the login page
# 
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """The Login View"""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        error = None
        
        user = User.query.filter_by(email=email).first()
        
        if error:
            flash(error)
        else:
            if user and check_password_hash(user.password, password):
                login_user(user)
                user.last_login = datetime.now()
                db.session.commit()

                # Check if user has the role of 'Voter' or 'Super'
                roles = [role.name for role in user.roles] 

                if 'Voter' in roles:
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('account.profile'))
                elif 'Super' in roles or 'Admin' in roles:
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash(f"Unknown role '{roles}', unable to determine where to redirect.", "danger")
                    return redirect(url_for('auth.login'))
                # flash("Logged in successfully!", "success")
                # return redirect(url_for('admin.dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html', form=form, title='Login')



#
# This is the Logout Route. It returns the logout page
# 
@auth.route('/logout/')
@login_required
def logout():
    """The Logout view"""
    # session.clear()
    logout_user()
    # Flash a logout message
    flash("You have been successfully logged out!", "success")
    return render_template('auth/logout.html', title='Logout')



#
# This is the Role Required Route. It returns the rolerequired page
# 
def role_required(*role_names):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if not any(role.name in role_names for role in current_user.roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# def role_required(roles):
#     """The Role Required View"""
#     if not isinstance(roles, list):
#         roles = [roles]  # Ensure roles is a list

#     def decorator(f):
#         @wraps(f)
#         @login_required
#         def decorated_function(*args, **kwargs):
#             # Query to check if the current user has one of the required roles
#             role = Role.query.filter(Role.name.in_(roles)).first()
#             if role is None:
#                 abort(403)  # None of the roles exist

#             user_role = UserRole.query.filter_by(user_id=current_user.id, role_id=role.id).first()
#             if user_role is None:
#                 abort(403)  # User does not have the required role
            
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

#===End=of=Auth=routes==========================================#
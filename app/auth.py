"""Authentication configuration file that contains auth views and routes."""
import functools
from models import *
from forms import *
from flask import (Blueprint, flash, g, redirect, render_template, session, url_for, abort)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .extensions import login_manager
from datetime import datetime
from functools import wraps

# login_manager = LoginManager()
auth = Blueprint('auth', __name__, url_prefix='/auth')


#=================================================================#
# Authorization routes section starts Here
# Contains all Authorization routes and any associated routes
#=================================================================#

#
# This is the Register Route. It returns the register page
# 
@auth.route('/register/', methods=('GET', 'POST'))
def register():
    """
    Register View
    """
    form = RegisterForm()
    form.roles.choices = [(r.id, r.name) for r in Role.query.filter(Role.name != 'Super').all()]
    
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        roles = form.roles.data

        error = None

        # if not firstname:
        #     error = "Firstname is required!"
        # elif not lastname:
        #     error = "Lastname is required!"
        # elif not email:
        #     error = "Email is required!"
        # elif not password:
        #     error = "Password is required!"

        validate_username = User.query.filter_by(username=(firstname+lastname)).first()
        validate_email = User.query.filter_by(email=email).first()

        if validate_username:
            error = f"Username {(firstname+lastname)} is taken. Please use a different username."
        elif validate_email:
            error = f"Email {email} is taken. Please use a different email address."

        if error:
            flash(error)
        else:
            try:
                user = User(username=(firstname+lastname), email=email, role=roles, 
                            date_registered=datetime.now(), updated_at=datetime.now())
                user.set_password(password)
                db.session.add(user)
                db.session.commit()


                flash(f"User {firstname+lastname} is added Successfully!", "success")
                return redirect(url_for('admin.settings'))
            except Exception as e:
                flash(f"There was an error saving data: {e}!", "danger")
                db.session.rollback
                return redirect(url_for('admin.settings'))
        flash(error)

    return render_template('auth/register.html', title='Register', form=form, ACCOUNT=True)


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

        # if not email:
        #     error = "Email is require!"
        # elif not password:
        #     error = "Password is required!"
        
        user = User.query.filter_by(email=email).first()
        
        if error:
            flash(error)
        else:
            if user and check_password_hash(user.password, password):
                login_user(user)
                user.last_login = datetime.now()
                db.session.commit()
                flash("Logged in successfully!", "success")
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
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
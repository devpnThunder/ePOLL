"""Settings configuration file that contains settings views and routes."""
from flask import (Blueprint, flash, redirect, render_template, url_for, request)
from flask_login import login_required, current_user
from datetime import datetime
from app.forms import RegistrationForm, ProfileForm
from app.auth import role_required
from app.models import Role, User, UserRole, Voter, Constituency
from app.extensions import db

accbp = Blueprint('account', __name__, url_prefix='/account')


#=================================================================#
# Voter routes section starts Here
# Contains all Voters routes and its associated routes
#=================================================================#
@accbp.route('/profile/')
# @login_required
# @role_required('Super')
def profile():
    """
    Load voter profile
    """
    count_voters = Voter.query.count()
    return render_template('pages/index.html', 
                           title='Voters',
                           count_voters=count_voters,
                           SETTINGS=True)



@accbp.route('/edit_profile/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_profile(id):
    """
    Edit Voter Profile route or 404 if not found
    """
    voter_profile = Voter.query.get_or_404(id)
    form = ProfileForm(obj=voter_profile)
    form.constituency_id.choices = [(c.id, c.name) for c in Constituency.query.all()]


    if form.validate_on_submit():
        voter_profile.constituency_id = form.constituency_id.data
        voter_profile.surname = form.surname.data
        voter_profile.firstname = form.firstname.data
        voter_profile.othername = form.othername.data
        voter_profile.gender = form.gender.data
        voter_profile.email = form.email.data
        voter_profile.password = form.password.data

        error = None

        if error:
            flash(error)
        else:
            try:
                # UserRole(user_id=selected_user.id, role_id=form.roles.data)
                db.session.commit()
                flash(f'{voter_profile.surname} is updated Successfully!', 'success')
                return redirect(url_for('voter.index'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('voter.index'))

    return render_template('pages/edit.html', title='Edit Profile', form=form, VOTER=True)


@accbp.route('/delete_account/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_account(id):
    """
    Delete User View or 404 if not found.
    """
    selected_voter = User.query.get_or_404(id)
    form = ProfileForm(obj=selected_voter)

    if form.validate_on_submit():
        try:
            db.session.delete(selected_voter)
            db.session.commit()
            flash('User is deleted successfully!', 'success')
            return redirect(url_for('voter.users'))
        except Exception as e:
            flash(f'There was an error during the deletion: {str(e)}!', 'danger')
            db.session.rollback()
            return redirect(url_for('voter.index'))

        
    return render_template('admin/settings/user/delete.html', title='Delete User', form=form, SETTINGS=True)
#===End=of=Voter=routes========================================#
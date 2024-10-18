"""Settings configuration file that contains settings views and routes."""
from flask import (Blueprint, flash, redirect, render_template, url_for, request)
from flask_login import login_required, current_user
from datetime import datetime
from app.forms import RegistrationForm, ProfileForm
from app.auth import role_required
from app.models import Role, User, UserRole, Voter, Constituency
from app.extensions import db, login_manager
from app.forms import *
from app.models import *

accbp = Blueprint('account', __name__, url_prefix='/account')


#=================================================================#
# Voter routes section starts Here
# Contains all Voters routes and its associated routes
#=================================================================#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@accbp.route('/profile/')
# @login_required
# @role_required('Super')
def profile():
    """
    Load voter profile
    """
    records = Voter.query.filter(Voter.user_id == current_user.id).all()
    count_voters = Voter.query.count()

    motionlist = Motion.query.filter(Motion.status == 'ACTIVE').all()
    return render_template('pages/index.html', 
                           title='Voters',
                           records=records,
                           count_voters=count_voters,
                           motionlist=motionlist,
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


#=================================================================#
# Motion routes section starts Here
# Contains all Motion routes and any associated routes
#=================================================================#
@accbp.route('/motions/')
# @login_required
# @role_required('Super', 'Admin')
def motions():
    """
    Load Motions list
    """
    count_motion = Motion.query.count()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    motionlist = Motion.query.order_by(Motion.created_at.desc()).paginate(page=page, per_page=page_size)
    if not motionlist:
        flash('No Motion records added Yet!', 'warning')

    return render_template('pages/index.html', count_motion=count_motion, motionlist=motionlist, POLLS=True)


@accbp.route('/newvote/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def newvote(id):
    """
    Create New Motion Vote
    """
    motion_check = Motion.query.get_or_404(id)
    form = MotionVoteForm()
    form.motion_id.choices = [(m.id, m.name) for m in Motion.query.filter(Motion.id == id)]

    if form.validate_on_submit():
        motion_id = form.motion_id.data
        vote = form.vote.data
        other_text = form.other_text.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newvote = MotionVote(voter_id=current_user.id, motion_id=motion_id, vote=vote, other_text=other_text, voted_at=datetime.now())
                db.session.add(newvote)
                db.session.commit()

                flash('Thank you for voting!', 'success')
                return redirect(url_for('aaccount.profile'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('account.profile'))
            
    return render_template('pages/motion.html', motion_check=motion_check, form=form, POLLS=True)
#===End=of=Motion=routes===========================================#


#=================================================================#
# Motion Agenda routes section starts Here
# Contains all Motion Agenda routes and any associated routes
#=================================================================#
@accbp.route('/agendas/')
# @login_required
# @role_required('Super', 'Admin')
def agendas():
    """
    Load Agendas list
    """
    count_agenda = Agenda.query.count()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    agendalist = Agenda.query.order_by(Agenda.created_at.desc()).paginate(page=page, per_page=page_size)
    if not agendalist:
        flash('No Agenda records added Yet!', 'warning')

    return render_template('pages/index.html', count_agenda=count_agenda, agendalist=agendalist, POLLS=True)


@accbp.route('/new_agendavote/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_agendavote(id):
    """
    Create New Agenda Vote
    """
    agenda_check = Agenda.query.get_or_404(id)
    form = AgendaVoteForm()
    form.agenda_id.choices = [(a.id, a.text) for a in Agenda.query.filter(Agenda.id == id)]

    if form.validate_on_submit():
        agenda_id = form.agenda_id.data
        vote = form.vote.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newvote = AgendaVote(voter_id=current_user.id, agenda_id=agenda_id, vote=vote, voted_at=datetime.now())
                db.session.add(newvote)
                db.session.commit()

                flash('Thank you for voting!', 'success')
                return redirect(url_for('account.profile'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('account.profile'))
            
    return render_template('pages/agenda.html', agenda_check=agenda_check, form=form, POLLS=True)

#===End=of=AgendaVote=routes===========================================#
#===End=of=Voter=routes========================================#
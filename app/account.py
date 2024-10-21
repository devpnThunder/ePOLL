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
    voter = Voter.query.filter(Voter.user_id == current_user.id).first()

    motionList = Motion.query.filter(Motion.status == 'PUBLISHED').all()


    if not voter:
        # Handle the case where the voter is not found
        flash('No voter profile found for the current user!', 'danger')
        return render_template('auth/login.html', title='Voters', SETTINGS=True)
    

    # Check if the voter has already voted
    for motion in motionList:
        check_if_vote = MotionVote.query.filter(MotionVote.voter_id == voter.id, MotionVote.motion_id == motion.id).first()

    if check_if_vote:
        flash('You have already voted', 'warning')


    count_isupport = MotionVote.query.filter(MotionVote.vote == 'ISUPPORT').count()
    count_idonotsupport = MotionVote.query.filter(MotionVote.vote == 'IDONOTSUPPORT').count()
    count_others = MotionVote.query.filter(MotionVote.vote == 'OTHERS').count()
    highest_count = max(count_isupport, count_idonotsupport, count_others)

    # Determine which category has the highest count
    if highest_count == count_isupport:
        highest_category = 'ISUPPORT'
    elif highest_count == count_idonotsupport:
        highest_category = 'IDONOTSUPPORT'
    else:
        highest_category = 'OTHERS'


    return render_template('pages/index.html', 
                           title='Voters',
                           voter=voter,
                           count_isupport=count_isupport,
                           count_idonotsupport=count_idonotsupport,
                           count_others=count_others,
                           highest_count=highest_count,
                           highest_category=highest_category,
                           motionList=motionList,
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


@accbp.route('/isupport/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def isupport(id):
    """
    Vote ISUPPORT
    """
    motion_check = Motion.query.get_or_404(id)

    error = None

    if error:
        flash(error)

    try:
        isupport = MotionVote(voter_id=current_user.id, motion_id=motion_check.id, vote=SupportOptions.ISUPPORT, voted_at=datetime.now())
        db.session.add(isupport)
        db.session.commit()

        flash('Thank you for voting!', 'success')
        return redirect(url_for('account.profile'))
    except Exception as e:
        flash(f'There was an error saving data: {e}!', 'danger')
        db.session.rollback
        return redirect(url_for('account.profile'))
    

@accbp.route('/idonotsupport/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def idonotsupport(id):
    """
    Vote IDONOTSUPPORT
    """
    motion_check = Motion.query.get_or_404(id)

    error = None

    if error:
        flash(error)

    try:
        isupport = MotionVote(voter_id=current_user.id, motion_id=motion_check.id, vote=SupportOptions.IDONOTSUPPORT, voted_at=datetime.now())
        db.session.add(isupport)
        db.session.commit()

        flash('Thank you for voting!', 'success')
        return redirect(url_for('account.profile'))
    except Exception as e:
        flash(f'There was an error saving data: {e}!', 'danger')
        db.session.rollback
        return redirect(url_for('account.profile'))
    

@accbp.route('/others/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def others(id):
    """
    Vote Others
    """

    motion_check = Motion.query.get_or_404(id)
    form = MotionVoteForm()
    # form.category_id.choices = [(c.id, c.name) for c in Category.query.filter(Category.name == SupportOptions.OTHERS)]

    if form.validate_on_submit():
        # motion_id = form.motion_id.data
        # vote = form.vote.data
        other_text = form.other_text.data

        error = None

        if error:
            flash(error)
        else:
            try:
                othervote = MotionVote(voter_id=current_user.id, motion_id=motion_check.id, vote=SupportOptions.OTHERS, other_text=other_text, voted_at=datetime.now())
                db.session.add(othervote)
                db.session.commit()

                flash('Thank you for voting!', 'success')
                return redirect(url_for('account.profile'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('account.profile'))
            
    return render_template('pages/motion.html', title='New Motion', form=form, POLLS=True)
            
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
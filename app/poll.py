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

pbp = Blueprint('poll', __name__, url_prefix='/poll')

#===================================================================================================#
# Admin View routes
# Contains all the routes and pages for Admin View Pages
#===================================================================================================#
#=================================================================#
# Motion routes section starts Here
# Contains all Motion routes and any associated routes
#=================================================================#
@pbp.route('/motions/')
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
    
    if not motionlist.items:
        flash('No motion records added yet!', 'info')

    return render_template('admin/poll/motion/list.html', title='Motion Polls', count_motion=count_motion, motionlist=motionlist, POLLS=True)


@pbp.route('/new_motion/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_motion():
    """
    Create New Motion
    """
    form = MotionForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        category_id = form.category_id.data
        name = form.name.data
        text = form.text.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newmotion = Motion(category_id=category_id, name=name, text=text, created_at=datetime.now())
                db.session.add(newmotion)
                db.session.commit()

                flash(f'{name} motion is created successfully!', 'success')
                return redirect(url_for('poll.motions'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('poll.motions'))
            
    return render_template('admin/poll/motion/create.html', title='New Motion', form=form, POLLS=True)


@pbp.route('/publish_motion/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def publish_motion(id):
    """
    Publish Motion View or 404 if not found
    """
    selected_motion = Motion.query.get_or_404(id)

    error = None

    if error:
        flash(error)

    try:
        selected_motion.status = MotionStatus.PUBLISHED
        db.session.commit()
        flash('Motion is published successfully!', 'success')
        return redirect(url_for('poll.motions'))
    except Exception as e:
        flash(f'There was an error during the publish: {e}!', 'danger')
        db.session.rollback()
        return redirect(url_for('poll.motions'))
    

@pbp.route('/close_motion/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def close_motion(id):
    """
    Close Motion View or 404 if not found
    """
    selected_motion = Motion.query.get_or_404(id)

    error = None

    if error:
        flash(error)

    try:
        selected_motion.status = MotionStatus.CLOSED
        db.session.commit()
        flash('Motion is closed successfully!', 'success')
        return redirect(url_for('poll.motions'))
    except Exception as e:
        flash(f'There was an error during the publish: {e}!', 'danger')
        db.session.rollback()
        return redirect(url_for('poll.motions'))


@pbp.route('/edit_motion/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_motion(id):
    """
    Edit Motion View or 404 if not found
    """
    selected_motion = Motion.query.get_or_404(id)
    form = MotionForm(obj=selected_motion)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        selected_motion.category_id = form.category_id.data
        selected_motion.name = form.name.data
        selected_motion.text = form.text.data
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(f'{selected_motion.name} motion is updated Successfully!', 'success')
                return redirect(url_for('poll.motions'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('poll.motions'))

    return render_template('admin/poll/motion/edit.html', title='Edit Motion', form=form, POLLS=True)


@pbp.route('/delete_motion/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_motion(id):
    """
    Delete Motion View or 404 if not found.
    """
    selected_motion = Motion.query.get_or_404(id)
    form = MotionForm(obj=selected_motion)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        try:
            db.session.delete(selected_motion)
            db.session.commit()
            flash('Motion is deleted successfully!', 'success')
            return redirect(url_for('poll.motions'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('poll.motions'))

        
    return render_template('admin/poll/motion/delete.html', title='Delete Motion', form=form, POLLS=True)
#===End=of=Motion=routes===========================================#



#=================================================================#
# Motion Poll routes section starts Here
# Contains all Motion Poll routes and any associated routes
#=================================================================#
@pbp.route('/motion_votes/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def motion_votes(id):
    """
    Load Motion Polls list page
    """
    votes = MotionVote.query.get_or_404(id)

    count_isupport = votes.query.filter(MotionVote.vote == 'ISUPPORT').count()
    count_idonotsupport = votes.query.filter(MotionVote.vote == 'IDONOTSUPPORT').count()
    count_others = votes.query.filter(MotionVote.vote == 'OTHERS').count()
    highest_count = max(count_isupport, count_idonotsupport, count_others)

    # Determine which category has the highest count
    if highest_count == count_isupport:
        highest_category = 'ISUPPORT'
    elif highest_count == count_idonotsupport:
        highest_category = 'IDONOTSUPPORT'
    else:
        highest_category = 'OTHERS'
    
    if not votes:
        flash('No motion vote records added yet!', 'info')

    return render_template('admin/poll/motion/votes.html', title='Motion Votes Results', 
                           votes=votes,
                           count_isupport=count_isupport,
                           count_idonotsupport=count_idonotsupport,
                           count_others=count_others,
                           highest_count=highest_count,
                           highest_category=highest_category,
                           POLLS=True)


@pbp.route('/newvote/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def newvote(id):
    """
    Create New Motion Vote
    """
    motion_check = Motion.query.get_or_404(id)
    form = MotionVoteOthersForm()
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
                return redirect(url_for('poll.motion_votes'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('poll.motion_votes'))
            
    return render_template('admin/poll/motionvote/vote.html', title='Vote', motion_check=motion_check, form=form, POLLS=True)

#===End=of=MotionPoll=routes===========================================#



#=================================================================#
# Motion Agenda routes section starts Here
# Contains all Motion Agenda routes and any associated routes
#=================================================================#
@pbp.route('/agendas/')
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
    
    if not agendalist.items:
        flash('No agenda records added yet!', 'info')

    return render_template('admin/poll/agenda/list.html', title='Agendas', count_agenda=count_agenda, agendalist=agendalist, POLLS=True)


@pbp.route('/new_agenda/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_agenda():
    """
    Create New Agenda
    """
    form = AgendaForm()
    form.motion_id.choices = [(m.id, m.name) for m in Motion.query.all()]

    if form.validate_on_submit():
        motion_id = form.motion_id.data
        text = form.text.data

        error = None

        if error:
            flash(error)
        else:
            try:
                newagenda = Agenda(motion_id=motion_id, text=text, created_at=datetime.now())
                db.session.add(newagenda)
                db.session.commit()

                flash('Agenda is added successfully!', 'success')
                return redirect(url_for('poll.agendas'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('poll.agendas'))
            
    return render_template('admin/poll/agenda/create.html', title='New Agenda', form=form, POLLS=True)


@pbp.route('/edit_agenda/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_agenda(id):
    """
    Edit Agenda View or 404 if not found
    """
    selected_agenda = Agenda.query.get_or_404(id)
    form = AgendaForm(obj=selected_agenda)
    form.motion_id.choices = [(m.id, m.name) for m in Motion.query.all()]

    if form.validate_on_submit():
        selected_agenda.motion_id = form.motion_id.data
        selected_agenda.text = form.text.data
        
        error = None

        if error:
            flash(error)
        else:
            try:
                db.session.commit()
                flash(' Agenda is updated Successfully!', 'success')
                return redirect(url_for('poll.agendas'))
            except Exception as e:
                flash(f'There was an error during the update: {e}!', 'danger')
                db.session.rollback()
                return redirect(url_for('poll.agendas'))

    return render_template('admin/poll/agenda/edit.html', title='Edit Agenda', form=form, POLLS=True)


@pbp.route('/delete_agenda/<int:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_agenda(id):
    """
    Delete Agenda View or 404 if not found.
    """
    selected_agenda = Agenda.query.get_or_404(id)
    form = AgendaForm(obj=selected_agenda)
    form.motion_id.choices = [(m.id, m.name) for m in Motion.query.all()]

    if form.validate_on_submit():
        try:
            db.session.delete(selected_agenda)
            db.session.commit()
            flash('Agenda is deleted successfully!', 'success')
            return redirect(url_for('poll.agendas'))
        except Exception as e:
            flash(f'There was an error during the deletion: {e}!', 'danger')
            db.session.rollback()
            return redirect(url_for('poll.agendas'))

        
    return render_template('admin/poll/agenda/delete.html', title='Delete Agenda', form=form, POLLS=True)
#===End=of=MotionViolations=routes===========================================#



#=================================================================#
# Agenda Vote routes section starts Here
# Contains all Agenda Vote routes and any associated routes
#=================================================================#
@pbp.route('/agenda_votes/<int:id>/')
# @login_required
# @role_required('Super', 'Admin')
def agenda_votes(id):
    """
    Load Agenda Votes list page
    """
    # Query to get all agendas
    agendas = Agenda.query.all()
    votes = MotionVote.query.get_or_404(id)

    agenda_vote_data = []

    for agenda in agendas:
        agenda_id = agenda.id

        total_votes = AgendaVote.query.filter_by(agenda_id=agenda_id).count()
        yes_votes = AgendaVote.query.filter_by(agenda_id=agenda_id, vote='True').count()
        no_votes = AgendaVote.query.filter_by(agenda_id=agenda_id, vote='False').count()
        
        agenda_vote_data.append({
            'agenda': agenda,
            'text': agenda.text,
            'total_votes': total_votes,
            'yes_votes': yes_votes,
            'no_votes': no_votes
        })
    

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)  # Get page size from query params or default to 20
    agendavoteList = AgendaVote.query.order_by(AgendaVote.voted_at.desc()).paginate(page=page, per_page=page_size)
    
    if not agendavoteList.items:  # `items` returns the records on the current page
        flash('No agenda vote records added yet!', 'info')

    return render_template('admin/poll/agendavote/list.html', title='Agenda Votes',
                           votes=votes,
                           agenda_vote_data=agenda_vote_data,
                           agendavoteList=agendavoteList,
                           POLLS=True)


@pbp.route('/new_agendavote/<int:id>/', methods=['GET', 'POST'])
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
                return redirect(url_for('poll.agenda_votes'))
            except Exception as e:
                flash(f'There was an error saving data: {e}!', 'danger')
                db.session.rollback
                return redirect(url_for('poll.agenda_votes'))
            
    return render_template('admin/poll/agendavote/vote.html', title='Agenda Vote', agenda_check=agenda_check, form=form, POLLS=True)

#===End=of=AgendaVote=routes===========================================#

#===End=of=Admin=routes=============================================================================#
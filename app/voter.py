"""Settings configuration file that contains settings views and routes."""
from flask import (Blueprint, flash, redirect, render_template, url_for, request)
from flask_login import login_required, current_user
from datetime import datetime
from app.forms import NewVoterForm, ProfileForm
from app.auth import role_required
from app.models import Role, User, UserRole, Voter, Constituency
from app.extensions import db

vbp = Blueprint('voter', __name__, url_prefix='/voter')


#=================================================================#
# Voter routes section starts Here
# Contains all Voters routes and its associated routes
#=================================================================#
@vbp.route('/voters/')
# @login_required
# @role_required('Super')
def voters():
    """
    Load all available voters
    """
    count_voters = Voter.query.count()
    return render_template('pages/index.html', 
                           title='Voters',
                           count_voters=count_voters,
                           SETTINGS=True)


@vbp.route('/voters/', methods=["GET", "POST"])
# @login_required
# @role_required('Super', 'Admin')
def voters():
    """available voters
    """
    search = request.args.get('search', '') # Search query from input box
    sort_by = request.args.get('sort_by', 'date_registered')  # Default sorting by date_registered
    sort_order = request.args.get('sort_order', 'asc')  # Default sorting order is ascending
    query = Voter.query

    if not query:
        flash('No Voter records added Yet!', 'warning')

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
    all_voters = query.order_by(Voter.date_registered.desc()).paginate(page=page, per_page=page_size)

    return render_template('admin/voter/index.html', title='Voters', all_voters=all_voters, sort_by=sort_by, sort_order=sort_order, page_size=page_size, VOTERS=True)


@vbp.route('/new_voter/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def new_voter():
    """
    Create New User
    """
    form = NewVoterForm()
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

        test = Voter.query.filter_by(email=email).first()

        if error:
            flash(error)
        else:
            if test:
                flash(f'{email} already exists!', 'warning')
                return redirect(url_for('voter.new_voter'))
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

                    flash(f'Account for {(firstname + ' ' + surname)}  is created successfully!', 'success')
                    return redirect(url_for('voter.index'))
                except Exception as e:
                    flash(f'There was an error saving data: {e}!', 'danger')
                    db.session.rollback
                    return redirect(url_for('voter.new_voter'))
            
    return render_template('pages/settings/index.html', title='New Voter', form=form, VOTER=True)


@vbp.route('/edit_profile/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super')
def edit_profile(id):
    """
    Edit Voter Profile route or 404 if not found
    """
    voter_profile = Voter.query.get_or_404(id)
    form = EditProfileForm(obj=voter_profile)
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


@vbp.route('/delete_voter/<string:id>/', methods=['GET', 'POST'])
# @login_required
# @role_required('Super', 'Admin')
def delete_voter(id):
    """
    Delete User View or 404 if not found.
    """
    selected_voter = User.query.get_or_404(id)
    form = ProfileForm(obj=selected_voter)
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
#===End=of=Voter=routes========================================#
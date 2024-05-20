# views.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import db, AlumniProfile, Role, User
from .forms import AlumniProfileForm
from .auth import roles_required, role_required  # Ensure this import is correct

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
@roles_required(Role.REGISTERED_ALUMNI, Role.ADMIN, Role.APPLIED_ALUMNI)
def view_profile():
    profile = profile = AlumniProfile.query.filter(
        AlumniProfile.user_id == current_user.id,
        AlumniProfile.full_name.isnot(None),
        AlumniProfile.school.isnot(None),
        AlumniProfile.graduation_year.isnot(None),
        AlumniProfile.bio.isnot(None)
    ).first()

    if not profile:
        return redirect(url_for('views.create_profile'))
    
    form = AlumniProfileForm()  # Instantiate the form object
    return render_template('profile.html', profile=profile, form=form, user=current_user)

@views.route('/profile/create', methods=['GET', 'POST'])
@login_required
@roles_required(Role.REGISTERED_ALUMNI, Role.ADMIN, Role.APPLIED_ALUMNI)
def create_profile():
    form = AlumniProfileForm()
    if form.validate_on_submit():
         # Check if email is already used
        existing_profile = AlumniProfile.query.filter_by(email=form.email.data).first()
        if existing_profile:
            flash('Email is already associated with another profile. Please use a different email.', 'error')
            return redirect(url_for('views.view_profile'))

        profile = AlumniProfile(
            user_id=current_user.id,
            full_name=form.full_name.data,
            school=form.school.data,
            graduation_year=form.graduation_year.data,
            bio=form.bio.data
        )
        db.session.add(profile)
        db.session.commit()
        flash('Profile created successfully.', 'success')
        return redirect(url_for('views.view_profile'))
    else:
        # Render the form with validation errors
        flash('Error creating profile. Please check your input.', 'error')
    return render_template('create_profile.html', form=form, user=current_user)

@views.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@roles_required(Role.REGISTERED_ALUMNI, Role.ADMIN)
def edit_profile():
    profile = AlumniProfile.query.filter_by(user_id=current_user.id).first_or_404()
    form = AlumniProfileForm(obj=profile)
    if form.validate_on_submit():
        profile.full_name = form.full_name.data
        profile.school = form.school.data
        profile.graduation_year = form.graduation_year.data
        profile.bio = form.bio.data
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('views.view_profile'))
    return render_template('edit_profile.html', form=form)

@views.route('/profiles')
@login_required
@roles_required(Role.ADMIN, Role.REGISTERED_ALUMNI)
def list_profiles():
    profiles = AlumniProfile.query.with_entities(AlumniProfile.id, AlumniProfile.full_name).all()
    return render_template('profiles.html', profiles=profiles, user=current_user)

@views.route('/profile/edit/<int:profile_id>', methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def edit_profile_admin(profile_id):
    profile = AlumniProfile.query.get_or_404(profile_id)
    form = AlumniProfileForm(obj=profile)
    if form.validate_on_submit():
        profile.full_name = form.full_name.data
        profile.school = form.school.data
        profile.graduation_year = form.graduation_year.data
        profile.bio = form.bio.data
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('views.list_profiles'))
    return render_template('edit_profile.html', form=form, profile=profile, user=current_user)

@views.route('/admin')
@login_required
@role_required(Role.ADMIN)
def admin_dashboard():
    return render_template('admin_dashboard.html')

@views.route('/alumni')
@login_required
@roles_required(Role.ADMIN, Role.REGISTERED_ALUMNI)
def alumni_dashboard():
    return render_template('alumni_dashboard.html')

@views.route('/apply')
@login_required
@roles_required(Role.VISITOR)
def apply_alumni():
    return render_template('apply_alumni.html')

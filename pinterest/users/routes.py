from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from pinterest.users.form import RegistrationForm, LoginForm, UpdateAccForm
from pinterest.models import User, Pin, UserInterest, Tags
from pinterest import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from pinterest.users.utils import selected_user_tags,save_pic

users = Blueprint('users',__name__)

# route for login-------------------------------------------------
@users.route("/login", methods=['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Successfully logged in...!!!', 'success')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home_page'))
        else:
            flash('Login unsuccessfully. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# route for register------------------------------------------------
@users.route("/register", methods=['POST', 'GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RegistrationForm()
    tags = Tags.query.all()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        interests = request.form.getlist('interest')

        for interest in interests:
            user_interest = UserInterest(user_id=user.id, tag_id=interest)
            db.session.add(user_interest)

        db.session.commit()
        flash(f'Account created for {form.username.data}!!!...', 'success')
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title='Registration', form=form, tags=tags)

# route for update profile--------------------------------------------------
@users.route("/profile", methods=['POST', 'GET'])
@login_required
def profile_page():
    form = UpdateAccForm()
    tags = Tags.query.all()
    user_tags = UserInterest.query.filter_by(user_id=current_user.id).all()
    selected_tags = selected_user_tags(user_tags)
    interests = request.form.getlist('interests')

    pins = Pin.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        if form.profile_pic.data:
            profile_name = save_pic(form.profile_pic.data)
            current_user.profile_pic = profile_name

        if selected_tags != interests:
            # for delete interest--------------------
            for selected_tag in selected_tags:
                if selected_tag not in interests:
                    UserInterest.query.filter_by(tag_id=selected_tag, user_id=current_user.id).delete()
                    db.session.commit()

            # for update add new interests------------------------
            for interest_id in interests:
                if interest_id not in selected_tags:
                    user_interest = UserInterest(user_id=current_user.id, tag_id=interest_id)
                    db.session.add(user_interest)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.!', 'success')
        return redirect(url_for('users.profile_page'))

    # current user data------------------------------------------
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic = url_for('static', filename='profile_img/' + current_user.profile_pic)
    return render_template('profile.html', title='profile', form=form, profile_pic=profile_pic, tags=tags,
                           selected_tags=selected_tags, pins=pins)

# route for log out---------------------------------------
@users.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out...!!!', 'success')
    return redirect(url_for('main.home_page'))

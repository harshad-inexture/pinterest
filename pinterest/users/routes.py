from flask import Blueprint, session, render_template, flash, redirect, url_for, request
from pinterest.users.form import RegistrationForm, LoginForm, UpdateAccForm, RequestResetForm, ResetPasswordForm
from pinterest.main.form import SearchForm
from pinterest.models import User, Pin, UserInterest, Tags, SavePin, Board
from pinterest import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from pinterest.users.utils import selected_user_tags, save_pic
from flask_mail import Message
from flask.views import View

users = Blueprint('users', __name__)


# route for login-------------------------------------------------
# @users.route("/login", methods=['POST', 'GET'])
# def login_page():
#     if current_user.is_authenticated:
#         session.permanent = True
#         return redirect(url_for('main.home_page'))
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             flash('Successfully logged in...!!!', 'success')
#
#             if next_page:
#                 return redirect(next_page)
#             else:
#                 return redirect(url_for('main.home_page'))
#         else:
#             flash('Login unsuccessfully. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

class LoginPage(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            session.permanent = True
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


users.add_url_rule('/login', view_func=LoginPage.as_view('login_page'))


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
    user_save_pins = SavePin.query.filter_by(user_id=current_user.id).all()
    user_tags = UserInterest.query.filter_by(user_id=current_user.id).all()
    selected_tags = selected_user_tags(user_tags)
    interests = request.form.getlist('interests')
    pins = Pin.query.filter_by(user_id=current_user.id).all()
    boards = Board.query.filter_by(user_id=current_user.id).all()

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
                           selected_tags=selected_tags, pins=pins, user_save_pins=user_save_pins,boards=boards)


# route for log out---------------------------------------
@users.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out...!!!', 'success')
    return redirect(url_for('main.home_page'))


# Show profile of users------------------------------------------
@users.route("/profile/<string:username>")
def user_profile(username):
    form = SearchForm()
    user_pro = User.query.filter_by(username=username).first()
    pins = Pin.query.filter_by(user_id=user_pro.id).all()
    profile_pic = url_for('static', filename='profile_img/' + user_pro.profile_pic)
    return render_template('user_profile.html', title=username, user=user_pro, profile_pic=profile_pic, pins=pins,
                           form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='inexture@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password.', 'info')
        return redirect(url_for('users.login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login_page'))
    return render_template('reset_token.html', title='Reset Password', form=form)

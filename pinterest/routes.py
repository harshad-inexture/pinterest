from flask import render_template, flash, redirect, url_for, request,abort
from pinterest.form import RegistrationForm, LoginForm, UpdateAccForm, NewPostForm, UpdatePostForm
from pinterest.models import User, Pin, UserInterest, Tags
from pinterest import app, db, bcrypt
import secrets, os
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required

# routes-----------------------------------------------------------------------------------

@app.route("/", methods=['POST', 'GET'])
def home_page():
    pins = Pin.query.all()
    return render_template('home.html', pins=pins)


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    profile_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', profile_fn)

    pic_size = (150, 150)
    i = Image.open(form_pic)
    i.thumbnail(pic_size)

    i.save(picture_path)
    return profile_fn

def selected_user_tags(user_tags):
    selected_tags = []
    for i in user_tags:
        selected_tags.append(i.tag_id)
    return selected_tags

@app.route("/profile", methods=['POST', 'GET'])
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
        return redirect(url_for('profile_page'))

    # current user data------------------------------------------
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic = url_for('static', filename='profile_img/' + current_user.profile_pic)
    return render_template('profile.html', title='profile', form=form, profile_pic=profile_pic, tags=tags,
                           selected_tags=selected_tags, pins=pins)


@app.route("/register", methods=['POST', 'GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
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
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Registration', form=form, tags=tags)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
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
                return redirect(url_for('home_page'))
        else:
            flash('Login unsuccessfully. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out...!!!', 'success')
    return redirect(url_for('home_page'))


def save_pin_img(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pin_pic_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pin_img', pin_pic_fn)

    i = Image.open(form_pic)
    i.save(picture_path)
    return pin_pic_fn


@app.route("/pin/new", methods=['POST', 'GET'])
@login_required
def new_pin():
    form = NewPostForm()
    tags = Tags.query.all()
    if form.validate_on_submit():
        if form.post_img.data:
            pin_pic = save_pin_img(form.post_img.data)
            pin = Pin(title=form.title.data, pin_pic=pin_pic, content=form.content.data, tag=form.img_tag.data,
                      user_id=current_user.id)
            db.session.add(pin)
            db.session.commit()
            flash('Your post has been created...!!!', 'success')
            return redirect(url_for('home_page'))
    return render_template('new_post.html', title='New Post', form=form, tags=tags)

@app.route("/pin/<int:pin_id>")
def selected_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get_or_404(pin.user_id)
    return render_template('pin.html',title=pin.title,pin=pin,user=user)

@app.route("/pin/<int:pin_id>/update", methods=['POST', 'GET'])
@login_required
def update_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get_or_404(pin.user_id)
    form = UpdatePostForm()
    tags = Tags.query.all()
    if pin.author != current_user:
        abort(403)
    if form.validate_on_submit():
        pin.title=form.title.data
        pin.content=form.content.data
        pin.tag=form.img_tag.data
        db.session.commit()
        flash('Your pin has been updated.!', 'success')
        return redirect(url_for('update_pin',pin_id=pin.id))
    if request.method == 'GET':
        form.title.data = pin.title
        form.content.data = pin.content

    return render_template('update_pin.html',title=pin.title,pin=pin,user=user,form=form,tags=tags)

@app.route("/pin/<int:pin_id>/delete", methods=['POST'])
@login_required
def delete_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    if pin.author != current_user:
        abort(403)
    db.session.delete(pin)
    db.session.commit()
    flash('Your pin has been deleted.!', 'success')
    return redirect(url_for('profile_page'))
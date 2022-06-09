from flask import render_template,flash,redirect,url_for,request
from pinterest.form import RegistrationForm,LoginForm
from pinterest.models import User,Pin,UserInterest,Tags
from pinterest import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required

# routes-----------------------------------------------------------------------------------

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/profile")
@login_required
def profile_page():
    return render_template('profile.html',title='profile')

@app.route("/register", methods=['POST','GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form=RegistrationForm()
    tags=Tags.query.all()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        interests = request.form.getlist('interest')
        for interest in interests:
            user_interest = UserInterest(user_id = user.id, tag_id=interest)
            db.session.add(user_interest)
        db.session.commit()
        flash(f'Account created for {form.username.data}!!!...','success')
        return redirect(url_for('login_page'))
    return render_template('register.html',title='Registration',form=form,tags=tags)

@app.route("/login", methods=['POST','GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Successfully logged in...!!!','success')
            if next_page:
                return redirect(next_page)
            else:
                return  redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pinterest.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        same_user = User.query.filter_by(username=username.data).first()
        if same_user:
            raise ValidationError('That username is taken please choose another one.')

    def validate_email(self, email):
        same_email = User.query.filter_by(email=email.data).first()
        if same_email:
            raise ValidationError('That email is taken please choose another one.')

class UpdateAccForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            same_user = User.query.filter_by(username=username.data).first()
            if same_user:
                raise ValidationError('That username is taken please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            same_email = User.query.filter_by(email=email.data).first()
            if same_email:
                raise ValidationError('That email is taken please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Log in')


# post form---------------------------------
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    post_img = FileField('Pin Image', validators=[FileAllowed(['jpg', 'png','jpeg']), DataRequired()])
    img_tag = StringField('Image Tag', validators=[DataRequired()])
    post = SubmitField('Post')

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    img_tag = StringField('Image Tag', validators=[DataRequired()])
    update = SubmitField('Update')

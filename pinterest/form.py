from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired , Length, Email, EqualTo,ValidationError
from pinterest.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=25)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        sameuser = User.query.filter_by(username=username.data).first()
        if sameuser:
            raise ValidationError('That username is taken please choose another one.')

    def validate_email(self,email):
        sameemail = User.query.filter_by(email=email.data).first()
        if sameemail:
            raise ValidationError('That email is taken please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Log in')
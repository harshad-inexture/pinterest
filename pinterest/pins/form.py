from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


# post form---------------------------------
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    post_img = FileField('Pin Image', validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    img_tag = StringField('Image Tag', validators=[DataRequired()])
    post = SubmitField('Post')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    img_tag = StringField('Image Tag', validators=[DataRequired()])
    update = SubmitField('Update')


# new board --------------------------------
class NewBoardForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    create = SubmitField('Create')


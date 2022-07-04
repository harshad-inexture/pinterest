from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateTagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    update = SubmitField('Update')


class BlockUserMsg(FlaskForm):
    reason = StringField('Reason', validators=[DataRequired()])
    block = SubmitField('Block')

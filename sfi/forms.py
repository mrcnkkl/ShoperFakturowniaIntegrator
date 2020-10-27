from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MailForm(FlaskForm):
    subject = StringField(label='subject', validators=[DataRequired()])
    message = StringField(label='message', validators=[DataRequired()])

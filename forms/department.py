from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Department', validators=[DataRequired()])
    chief = IntegerField("Chief ID")
    members = StringField("Members")
    email = StringField('email')
    submit = SubmitField('Submit')

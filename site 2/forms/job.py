from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField("Team Leader ID")
    work_size = IntegerField("Work Size")
    collaborators = StringField('Collaborators')
    is_finished = BooleanField("Is job finished?")
    category = SelectField('Category', choices=["1", '2', '3'])
    submit = SubmitField('Submit')

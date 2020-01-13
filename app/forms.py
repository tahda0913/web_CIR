from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Regexp
from app import db
from app.models import get_school_list, get_incident_types, get_crisis_response

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter your username")])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CIRForm(FlaskForm):
    incident_date = DateField('Incident Date', format='%Y-%m-%d', validators=[DataRequired(message="Please enter Date of Incident")])
    school_name = SelectField('School Name', validators=[DataRequired()], choices=[(school, school) for school in get_school_list()])
    incident_type = SelectField('Incident Type', validators=[DataRequired()], choices=[(incident, incident) for incident in get_incident_types()])
    incident_narrative = TextAreaField('Incident Narrative', validators=[DataRequired()])
    comments = TextAreaField('Additional Comments')
    phys_restraint = BooleanField('Physical Restraint')
    police = BooleanField('Police')
    phys_harm = BooleanField('Physical Harm')
    fire_rescue = BooleanField('Fire or Rescue')
    dcyf = BooleanField('DCYF')
    risk_assessment = BooleanField('Suicide Risk Assessment Administered')
    cteam_response = SelectField('Crisis Team Response for Suicidal Ideation', choices=[(response, response) for response in get_crisis_response()])
    submit = SubmitField('Submit Form')

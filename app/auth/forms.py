from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import db
from app.auth import bp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter your username")])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

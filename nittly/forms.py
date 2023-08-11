from flask_wtf import FlaskForm
""" from flask_wtf.file import FileField, FileAllowed """
""" from flask_login import current_user """
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from nittly.models import User,Url

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email')

class LoginForm(FlaskForm):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember me')
    submit= SubmitField('Login')


class UrlForm(FlaskForm):
    original_url = StringField('URL', validators=[DataRequired()])
    short_id = StringField('Backoff (Optional)',validators=[])
    submit = SubmitField('Generate URL')

    def validate_short_id(self,short_id):
        url_short_id=Url.query.filter_by(short_id=short_id.data).first()
        if url_short_id:
            raise ValidationError('That Backoff is taken. Please choose a different one')


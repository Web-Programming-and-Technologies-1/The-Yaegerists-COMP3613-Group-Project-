from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email
from flask_wtf.file import FileField

class SignUp(FlaskForm):
    username = StringField('Enter Username', validators=[InputRequired()])
    #name = StringField('name', validators=[InputRequired()])
    email = StringField('Enter Email', validators=[Email(), InputRequired()])
    password = PasswordField('Enter New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class LogIn(FlaskForm):
    username = StringField('Enter Username', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})

class UploadPicture(FlaskForm):
    #username = StringField('Username')
    url = StringField('URL:', validators=[InputRequired()])
    #image = FileField("Upload Profile Image:")
    submit = SubmitField('Upload Image', render_kw={'class': 'btn waves-effect waves-light white-text'})
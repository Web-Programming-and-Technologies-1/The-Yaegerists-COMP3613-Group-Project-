import flask_login
from flask_jwt import JWT
from App.models import Profile

#Added error handling to the functions below provided within the MVC template
def authenticate(username, password):
    user = Profile.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return Profile.query.get(payload['identity'])

#Remember a user login details 
def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)

#Allow user to logout of the system once logged in
def logout_user():
    flask_login.logout_user()

def setup_jwt(app):
    return JWT(app, authenticate, identity)
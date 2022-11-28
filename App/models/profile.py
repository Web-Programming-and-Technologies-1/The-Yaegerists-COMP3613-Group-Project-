from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask import jsonify


class Profile(db.Model):
    profileId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # what does this hold? can it be null?
    recipients = db.Column(db.String(120), unique=True, nullable=False)
    # what does this hold? can it be null? is feed and profile feed the same thing?
    feed = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.relationship('ProfileFeed', backref='profile',
                              lazy=True, cascade="all, delete-orphan")

    # should recipients and feed be initialized?
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
            # what else to return? im unsure about what the attribute holds
        }

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # what does this function do/get
    def get_feed():
        pass

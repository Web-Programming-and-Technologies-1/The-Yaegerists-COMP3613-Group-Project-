from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask import jsonify


class Profile(db.Model):
    profileId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    recipients = db.relationship('ProfileFeed', backref='recipients',
                                 lazy=True, cascade="all, delete-orphan")
    feeds = db.relationship('ProfileFeed', backref='feeds',
                           lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return {
            'profileId': self.id,
            'username': self.username,
            'email': self.email,
            'recipients': [recipient.toJSON() for recipient in self.recipients],
            'feeds': [feed.toJSON() for feed in self.feeds]
        }

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

   

from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin
from .profile_feed import*
from flask import jsonify 


class Profile(db.Model, UserMixin):
    profileId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # recipients = db.relationship('ProfileFeed', primaryjoin="Profile.profileId==ProfileFeed.senderId")
    # feeds = db.relationship('ProfileFeed', primaryjoin="Profile.profileId==ProfileFeed.receiverId")
    image = db.relationship('Image', backref='profile',lazy=True, cascade="all, delete-orphan")
    overall_rating = db.Column(db.Integer)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def get_id(self):
        return (self.profileId)

    def set_overall_rating(self, rating):
        self.overall_rating = rating

    def get_overall_rating(self):
        return (self.overall_rating)
        
    def toJSON(self):
        return {
            'profileId': self.profileId,
            'username': self.username,
            'email': self.email,
            # 'recipients': [recipient.toJSON() for recipient in self.recipients],
            # 'feeds': [feed.toJSON() for feed in self.feeds],
            'overall_rating': self.overall_rating
        }

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    

from App.database import db
from datetime import date

# Ratings are created by users when they rate other users' profiles
# Timestamps solve the 'limited number of ratings a day' problem
class Rating(db.Model):
    ratingId = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)  
    username = db.Column(db.String(120), db.ForeignKey('profile.username'))
    score = db.Column(db.Integer,unique=False, nullable=False)
    timeStamp = db.Column(db.Date, nullable=False)

    def __init__(self,senderId, receiverId ,score):
        self.senderId = senderId
        self.receiverId = receiverId
        self.username = username
        self.score = score
        self.timeStamp = date.today()

    def toJSON(self):
        return {
            'id': self.ratingId,
            'senderId': self.senderId,
            'receiverId': self.receiverId,
            'username': self.username,
            'score': self.score,
            'timeStamp': self.timeStamp
        }

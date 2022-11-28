from App.database import db
from datetime import date

# Ratings are created by users when they rate other users' profiles
# Timestamps solve the 'limited number of ratings a day' problem


class Rating(db.Model):
    ratingId = db.Column(db.Integer, primary_key=True)
    # whats the purpose of this?
    creatorId = db.Column(db.Integer,  nullable=False)
    targetId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)  # ''''
    score = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.Date, nullable=False)

    def __init__(self, creatorId, targetId, score):
        self.creatorId = creatorId
        self.targetId = targetId
        self.score = score
        self.timeStamp = date.today()

    def toJSON(self):
        return {
            'id': self.id,
            'creatorId': self.creatorId,
            'targetId': self.targetId,
            'score': self.score,
            'timeStamp': self.timeStamp
        }

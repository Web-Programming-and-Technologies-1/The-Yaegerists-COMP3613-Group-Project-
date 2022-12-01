from App.database import db

# Stores the Ranking details created by users when they rate other users' images
class Ranking(db.Model):
    rankingId = db.Column(db.Integer, primary_key=True)
    rankerId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    imageId = db.Column(db.Integer, db.ForeignKey(
        'image.imageId'), nullable=False)
    ratingId = db.Column(db.Integer, db.ForeignKey(
        'rating.ratingId'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self):
        self.score = 0

    def toJSON(self):
        return {
            'id': self.rankingId,
            'rankerId': self.rankerId,
            'imageId': self.imageId,
            'ratingId': self.ratingId,
            'score': self.score,
        }

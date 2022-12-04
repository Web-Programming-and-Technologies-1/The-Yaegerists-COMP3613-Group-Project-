from App.database import db

# Stores the Ranking details created by users when they rate other users' images
class Ranking(db.Model):
    rankingId = db.Column(db.Integer, primary_key=True)
    rankerId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    imageId = db.Column(db.Integer, db.ForeignKey(
        'image.imageId'), nullable=False)
    
    score = db.Column(db.Integer, nullable=False)
    overall_ranking = db.Column(db.Integer)
    def __init__(self, rankerId, imageId, score):
        self.rankerId= rankerId
        self.imageId = imageId
        self.score = score

    def toJSON(self):
        return {
            'id': self.rankingId,
            'rankerId': self.rankerId,
            'imageId': self.imageId,
            'score': self.score,
            'overall_ranking': self.overall_ranking
        }

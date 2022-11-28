from App.database import db

# Images uploaded by users


class Image(db.Model):
    imageId = db.Column(db.Integer, primary_key=True)
    profileId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    rankings = db.relationship(
        'Ranking', backref='ranking', lazy=True, cascade="all, delete-orphan")

    def __init__(self, profileId, rank):
        self.profileId = profileId
        self.rank = rank

    def toJSON(self):
        return {
            'id': self.id,
            'profileId': self.profileId,
            'rank': self.rank,
            'rankings': [ranking.toJSON() for ranking in self.rankings]
        }

    def get_final_ranking():
        pass
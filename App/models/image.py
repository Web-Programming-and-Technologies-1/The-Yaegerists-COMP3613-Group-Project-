from App.database import db


# Stores the Images uploaded by users
class Image(db.Model):
    imageId = db.Column(db.Integer, primary_key=True)
    profileId = db.Column(db.Integer, db.ForeignKey('profile.profileId'), nullable=False)
    url = db.Column(db.String(300),  nullable=False)
    rankings = db.relationship( 'Ranking', backref='image', lazy=True, cascade="all, delete-orphan")

    def __init__(self, profileId,url):
        self.profileId =profileId
        self.url = url

    def toJSON(self):
        return {
            'id': self.imageId,
            'profileId': self.profileId,
            'url':self.url,
            'rankings': [ranking.toJSON() for ranking in self.rankings]
        }

from App.database import db

# stores the user defined amount of randomly distributed profiles
class ProfileFeed(db.model):
    feedId = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    distributeId = db.Column(db.Integer, db.ForeignKey(
        'distribution.distributeId'), nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self):
        self.seen = True

    def toJSON(self):
        return {
            'feedId': self.feedId,
            'senderId': self.senderId,
            'receiverId': self.receiverId,
            'distributeId': self.distributeId,
            'seen': self.seen
        }

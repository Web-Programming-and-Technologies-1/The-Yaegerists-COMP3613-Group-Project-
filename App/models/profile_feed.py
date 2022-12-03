from App.database import db


# stores the user defined amount of randomly distributed profiles/profile feeds
class ProfileFeed(db.Model):
    feedId = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    distributeId = db.Column(db.Integer, db.ForeignKey(
        'distribution.distributeId'), nullable=False)
    sender = db.Column(db.Integer, nullable=False)
    receiver= db.Column(db.Integer, nullable=False)
    seen = db.Column(db.Boolean, default=False)

    def __init__(self, senderId, receiverId, distributorId):
        self.sender = senderId
        self.receiver = receiverId
        self.distributeId = distributorId
        self.seen = False

    def setSeen (self):
        self.seen = True
        
    def toJSON(self):
        return {
            'feedId': self.feedId,
            'senderId': self.sender,
            'receiverId': self.receiver,
            'distributeId': self.distributeId,
            'seen': self.seen
        }

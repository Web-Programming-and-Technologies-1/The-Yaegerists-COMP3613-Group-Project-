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
    seen = db.Column(db.Boolean, nullable=False)

    def __init__(self, senderId, receiverId):
        self.sender = senderId
        self.receiver = receiverId
        self.seen = True

    def toJSON(self):
        return {
            'feedId': self.feedId,
            'senderId': self.sender,
            'senderProfile': [senderProfile.toJSON() for senderProfile in self.senderId],
            'receiverId': self.receiver,
            'receiverProfile': [receiverProfile.toJSON() for receiverProfile in self.receiverId],
            'distributeId': self.distributeId,
            'seen': self.seen
        }

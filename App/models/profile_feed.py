from App.database import db


class ProfileFeed(db.model):
    feedId = db.Column(db.Integer, primary_key=True)
    # ?why does it have the same FK
    senderId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey(
        'profile.profileId'), nullable=False)
    distributeId = db.Column(db.Integer, db.ForeignKey(
        'distribution.distributeId'), nullable=False)
    # are these correct based on sir description? x2
    sender = db.Column(db.String(120), nullable=False)
    receiver = db.Column(db.String(120), nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)

    def toJSON(self):
        return {
            'feedId': self.feedId,
            'senderId': self.senderId,
            'receiverId': self.receiverId,
            'distributeId': self.distributeId,
            'sender': self.sender,
            'receiver': self.receiver,
            'seen': self.seen
        }

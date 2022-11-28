from App.database import db
from datetime import date

class Distribution(db.Model):
    profileId = db.Column(db.Integer, primary_key=True)
    numProfiles = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.Date , nullable=False)


    def distribute(self):
        return{
            'profileId': self.profileId,
            'numProfiles':self.numProfiles,
            'timeStamp':self.timeStamp
        }
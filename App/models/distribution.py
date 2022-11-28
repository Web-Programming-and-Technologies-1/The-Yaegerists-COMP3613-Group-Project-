from App.database import db
from datetime import date

class Distribution(db.Model):
    profileId = db.Column(db.Integer, primary_key=True)
    
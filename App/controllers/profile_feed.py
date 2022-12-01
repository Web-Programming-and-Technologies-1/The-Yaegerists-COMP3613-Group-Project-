from App.models import ProfileFeed
from App.database import db
from sqlalchemy.exc import IntegrityError

'''Create Operation'''
#Create a profile feed
def create_profile_Feed(senderId, receiverId):
    new_profile_feed = ProfileFeed(senderId, receiverId)
    try:
        db.session.add(new_profile_feed)
        db.session.commit()
        return new_profile_feed
    except IntegrityError:
        db.session.rollback()
    return None 

# get all profile feeds
def get_all_profile_feed():
    return ProfileFeed.query.all()
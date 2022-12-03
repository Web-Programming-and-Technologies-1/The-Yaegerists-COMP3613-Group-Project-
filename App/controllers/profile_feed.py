from App.models import ProfileFeed
from App.database import db
from sqlalchemy.exc import IntegrityError

from .profile import (
    get_profile
)

'''Create Operation'''
def create_profile_Feed(senderId, receiverId, distributeId):
    sender = get_profile(profileId= senderId)
    receiver = get_profile(profileId =receiverId)
    try:
        if sender and receiver:
            new_profile_feed = ProfileFeed(senderId=senderId, receiverId=receiverId, distributorId=distributeId)
            db.session.add(new_profile_feed)
            db.session.commit()
            return new_profile_feed
        return None
    except IntegrityError:
        db.session.rollback()
    return None 

'''Read Operation'''
def get_profile_feed(feedId):
    return ProfileFeed.query.filter_by(feedId=feedId).first()

def get_profile_feed_json(feedId):
    profile_feed = get_profile_feed(feedId)
    if profile_feed:
        return profile_feed.toJSON()
    return None

def get_all_profile_feed():
    return ProfileFeed.query.all()

def get_all_profile_feed_json():
    profile_feeds = get_all_profile_feed()
    if profile_feeds:
        return[profile_feed.toJSON() for profile_feed in profile_feeds]
    return None

def get_all_profile_feed_by_sender(senderId):
    return ProfileFeed.query.filter_by(senderId=senderId).all()

def get_all_profile_feed_by_sender_json(senderId):
    profile_feeds = get_all_profile_feed_by_sender(senderId)
    if profile_feeds:
        return[profile_feed.toJSON() for profile_feed in profile_feeds]
    return None

def get_all_profile_feed_by_receiver(receiverId):
    return ProfileFeed.query.filter_by(receiverId=receiverId).all()

def get_all_profile_feed_by_receiver_json(receiverId):
    profile_feeds = get_all_profile_feed_by_receiver(receiverId)
    if profile_feeds:
        return[profile_feed.toJSON() for profile_feed in profile_feeds]
    return None

def seen_profile_feeds(feedId):
    profile_feed = get_profile_feed(feedId)
    try:
        if profile_feed:
            profile_feed.setSeen()
            db.session.commit()
            return feed
        return None
    except:
        db.session.rollback()
    return None

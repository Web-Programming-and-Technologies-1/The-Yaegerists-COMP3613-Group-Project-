from App.models import Distribution, ProfileFeed
from App.database import db
import random
from sqlalchemy.exc import IntegrityError

from .profile import (
    get_all_profiles,
    get_profile
)

from .profile_feed import(
    create_profile_Feed
)
'''Create Operation'''
#Create a profile distribution
def create_distribution(numProfiles):
    new_profile = Distribution(numProfiles)
    try:
        db.session.add(new_profile)
        db.session.commit()
        return new_profile
    except IntegrityError:
        db.session.rollback()
    return None 

'''Read Operation'''
def get_distribution(distributeId):
    return Distribution.query.filter_by(distributeId=distributeId).first()

def get_distribution_json(distributionId):
    distribution = get_distribution(distributionId)
    if distribution:
        return distribution.toJSON()
    return None

def get_all_distributions():
    return Distribution.query.all()

def get_all_distributions_json():
    distributions = get_all_distributions()
    if distributions:
        return[distribution.toJSON() for distribution in distributions]
    return None

def get_profile_feeds(distributeId):
    profile_feed = get_distribution(distributeId)
    if profile_feed:
        return profile_feed.profileFeeds
    return None

# query all profiles
# shuffles all profiles found
# find the minimum number between available profiles and profiles requested
# while length of displayed rofile is less that the requested amount of profiles 
# get a random pfofile that isnt the logged in user
#create a profile distribution
#create a profile feed
# return the list of profiles to be displayed
# Return none otherwise
def distribute(numProfiles, senderId):
    distributeProfiles= get_all_profiles()
    if distributeProfiles:  
        random.shuffle(distributeProfiles)
        displayProfile= []  
        availableProfiles = min(numProfiles, len(distributeProfiles))    
        while len(displayProfile) < availableProfiles:          
            rand = random.randint(0, totalProfileNum)
            profile = get_profile(rand)
            if rand != senderId:
                displayProfile.append(profile)               
                create_distribution(availableProfiles)
                create_profile_Feed(senderId, rand)
        return displayProfile
         
    return None


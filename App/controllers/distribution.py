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


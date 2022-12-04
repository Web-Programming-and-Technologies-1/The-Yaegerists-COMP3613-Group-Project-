from App.models import Profile, Rating
from App.database import db
from sqlalchemy.exc import IntegrityError
from .rating import *

'''Create operations'''

#Create a new profile using the specified information USED
def create_profile(username, email,  password):
    if get_profile_by_username(username=username):
        return None
    new_profile = Profile(username=username, email=email, password=password)
    try:
        db.session.add(new_profile)
        db.session.commit()
        return new_profile
    except IntegrityError:
        db.session.rollback()
    return None  

'''Read operations'''
# Return profile with the specified username USED
def get_profile_by_username(username):
    return Profile.query.filter_by(username=username).first()
   
# Return profile with the specified Id USED
def get_profile(profileId):
    return Profile.query.filter_by(profileId=profileId).first()


# Return all profile USED
def get_all_profiles():
    return Profile.query.all()

#Gets and returns all profile in JSON format USED
def get_all_profiles_json():
    profiles = get_all_profiles()
    if profiles:
        return [profile.toJSON() for profile in profiles]
    return []

'''Update operations'''
# Get a profile based on profile ID
# Return none if profile not found
# Updates the profile details 
# Returns the updated profile
def update_profile(profileId, username, email,password):
    profile = get_profile(profileId)
    try:
        if profile:
            profile.username = username
            profile.email = email
            profile.password = password
            db.session.add(profile)
            db.session.commit()
            return profile
        return None
    except:
        db.session.rollback()
    return None
    
'''Delete Operations'''
# Get a profile based on profile ID
# Return false if profile not found
# Deletes the profile if found and return true
def delete_profile(profileId):
    profile = get_profile(profileId)
    try:
        if profile:
            db.session.delete(profile)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
    return False

def get_top_rated_Profiles():
    profiles = get_all_profiles()
    for profile in profiles:
        profile.overall_rating = get_total_rating(profile.profileId)
    return Profile.query.order_by(desc(Profile.overall_rating))



   
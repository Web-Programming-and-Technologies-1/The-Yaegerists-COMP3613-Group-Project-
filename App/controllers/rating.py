from App.models import Rating, Profile
from App.database import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from .profile import *

'''Create operations'''
#Create a rating to a specific profile
def create_rating(senderId, receiverId, score):
    new_rating = Rating(senderId=senderId, receiverId=receiverId, score=score)
    try:
        db.session.add(new_rating)
        db.session.commit()
        return new_rating
    except IntegrityError:
        db.session.rollback()
    return None  

'''Read operations'''
#gets a rating based on the specified rating ID
def get_rating(ratingId):
    return Rating.query.filter_by(ratingId=ratingId).first()

#gets a rating based on the specified receiver ID
def get_ratings_by_receiver(receiverId):
    return Rating.query.filter_by(receiverId=receiverId)

#gets a rating based on the specified sender ID
def get_ratings_by_sender(senderId):
    return Rating.query.filter_by(senderId=senderId)

#Gets all ratings
def get_all_ratings():
    return Rating.query.all()

#Gets all ratings and return the rating in JSON format or None otherwise
def get_all_ratings_json():
    ratings = get_all_ratings()
    if ratings:
        return[rating.toJSON() for rating in ratings]
    return None

# get ratings by receiver ID and returns the ratings in JSON format or None otherwise
def get_ratings_by_receiver_json(receiverId):
    ratings = get_ratings_by_receiver(receiverId)
    if ratings: 
        return [rating.toJSON() for rating in ratings]
    return None

# get ratings by sender ID and returns the ratings in JSON format or None otherwise
def get_ratings_by_sender_json(senderId):
    ratings = get_ratings_by_sender(senderId)
    if ratings:
        return [rating.toJSON() for rating in ratings]
    return None

# get ratings based on actors ID and returns the ratings in JSON format or None otherwise
def get_rating_by_actors(senderId, receiverId):
    # if get_profile(senderId) and get_profile(receiverId):
    if Profile.query.get(senderId) and Profile.query.get(receiverId):
        return  Rating.query.filter_by(senderId=senderId, receiverId=receiverId).first()  
    return None


'''Update operations'''
# Get a rating based on rating ID
# Return none if rating not found
# Updates the rating details if found
# Returns the updated rating or None otherwise
def update_rating(id, score):
    rating = get_rating(id)
    try:
        if rating:
            rating.score = score
            db.session.add(rating)
            db.session.commit()
            return rating
        return None
    except:
        db.session.rollback()
    return None
    
'''Delete Operations''' 
# Get a rating based n rating ID
# Return false if rating not found
# Deletes the rating if found and return true  
def delete_rating(id):
    rating = get_rating(id)
    try:
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
    return False

#Gets rating based on receiver Id and the average rating and return the avg rating or None otherwise
def get_calculated_rating(receiverId):
    ratings = get_ratings_by_receiver(receiverId)
    total = 0
    if ratings:
        for rating in ratings:
            total = total + rating.score
        if ratings.count() != 0:
            total = total / ratings.count()
        return total
    return None

#Gets total rating based on receiver Id and returns the total or None otherwise
def get_total_rating(receiverId):
    ratings = get_ratings_by_receiver(receiverId)
    total = 0
    if ratings:
        for rating in ratings:
            total = total + rating.score
        return total
    return None

#Gets the sender ratings and calculates the profile tier and returns the tier or None otherwise
def get_level(id):
    ratings = get_ratings_by_sender_json(id)
    if ratings:
        level = 0
        for rating in ratings:
            level = level + 1
        return level
    return None


def get_top_rated_profiles():
    return Rating.query.order_by(desc(Rating.score))
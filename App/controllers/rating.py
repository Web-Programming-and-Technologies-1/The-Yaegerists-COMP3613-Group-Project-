from App.models import Rating, Profile
from App.database import db
from sqlalchemy.exc import IntegrityError

'''Create operations'''
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
def get_ratings_by_target(receiverId):
    ratings = Rating.query.filter_by(receiverId=receiverId)
    if ratings: 
        return [rating.toJSON() for rating in ratings]
    return None

def get_ratings_by_creator(senderId):
    ratings = Rating.query.filter_by(senderId=senderId)
    if ratings:
        return [rating.toJSON() for rating in ratings]
    return None

def get_rating_by_actors(senderId, receiverId):
    if Profile.query.get(senderId) and Profile.query.get(receiverId):
        return  Rating.query.filter_by(senderId=senderId, receiverId=receiverId).first()  
    return None

def get_rating(ratingId):
    return Rating.query.filter_by(ratingId=ratingId).first()

def get_all_ratings():
    return Rating.query.all()

def get_all_ratings_json():
    ratings = Rating.query.all()
    if ratings:
        return[rating.toJSON() for rating in ratings]
    return None

'''Update operations'''
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
    
#what Use case is this - can be removed
def get_calculated_rating(receiverId):
    ratings = Rating.query.filter_by(receiverId=receiverId)
    total = 0
    if ratings:
        for rating in ratings:
            total = total + rating.score
        if ratings.count() != 0:
            total = total / ratings.count()
        return total
    return None

def get_level(id):
    ratings = get_ratings_by_creator(id)
    if ratings:
        level = 0
        for rating in ratings:
            level = level + 1
        return level
    return None
from App.models import Ranking
from App.database import db
from sqlalchemy.exc import IntegrityError

from .profile import(
    get_profile
)

from .image import (
    get_image
)

'''Create operations'''
#Create a ranking to a specific image
def create_ranking(rankerId, imageId, score):
    new_ranking = Ranking(rankerId=rankerId, imageId=imageId, score=score)
    try:
        db.session.add(new_ranking)
        db.session.commit()
        return new_ranking
    except IntegrityError:
        db.session.rollback()
    return None 

'''Read operations'''
# Return ranking with the specified ranker Id 
def get_rankings_by_ranker(rankerId):
    return Ranking.query.filter_by(rankerId=rankerId)

# Return ranking with the specified image Id 
def get_rankings_by_image(imageId):
    return Ranking.query.filter_by(imageId=imageId)

# Return ranking with the specified rank Id 
def get_ranking(id):
    return Ranking.query.get(id)

# Return all rankings
def get_all_rankings():
    return Ranking.query.all()

# gets all rankings and return the rankings in JSON format or None otherwise
def get_all_rankings_json():
    rankings = get_all_rankings()
    if rankings: 
        return [ranking.toJSON() for ranking in rankings]
    return None

# gets all rankings by ranker ID and return the rankings in JSON format or None otherwise
def get_rankings_by_ranker_json(rankerId):
    rankings = get_rankings_by_ranker(rankerId)
    if rankings:   
        return[ranking.toJSON() for ranking in rankings]
    return None

# gets all rankings by image ID and return the rankings in JSON format or None otherwise
def get_rankings_by_image_json(imageId):
    rankings = get_rankings_by_image(imageId)
    if rankings:
        return [ranking.toJSON() for ranking in rankings]
    return None

# gets all rankings made by a Profile  and return the rankings  or None otherwise
def get_ranking_by_actors(rankerId, imageId):
    if get_profile(rankerId) and get_image(imageId):
        return Ranking.query.filter_by(rankerId=rankerId, imageId=imageId).first()
    return None

'''Update operations'''
# Get a rank based on rank ID
# Return none if rank not found
# Updates the rank details if found
# Returns the updated rank or None otherwise
def update_ranking(id, score):
    ranking = get_ranking(id)
    try:
        if ranking:
            ranking.score = score
            db.session.add(ranking)
            db.session.commit()
            return ranking
        return None   
    except:
        db.session.rollback()
    return None

'''Delete Operations''' 
# Get a rank based n rank ID
# Return false if rank not found
# Deletes the rank if found and return true  
def delete_rank(id):
    rank = get_ranking(id)
    try:
        if rank:
            db.session.delete(rank)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
    return False


# Get all image rankings and get avergae rankings 
def get_calculated_ranking(imageId):
    rankings = get_rankings_by_image(imageId)
    total = 0
    if rankings:
        for ranking in rankings:
            total = total + ranking.score
        if rankings.count() != 0:
            total = total / rankings.count()
        return total
    return None

# Gets total ranking by imageId
def get_total_ranking(imageId):
    rankings = get_rankings_by_image(imageId)
    total = 0
    if rankings:
        for ranking in rankings:
            total = total + ranking.score
        return total
    return None



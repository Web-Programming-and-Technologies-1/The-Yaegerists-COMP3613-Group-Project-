from App.models import Ranking, Profile, Image
from App.database import db
from sqlalchemy.exc import IntegrityError

'''Create operations'''
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
def get_rankings_by_ranker(rankerId):
    return Ranking.query.filter_by(rankerId=rankerId)

def get_rankings_by_image(imageId):
    return Ranking.query.filter_by(imageId=imageId)

def get_ranking(id):
    return Ranking.query.get(id)
    
def get_all_rankings():
    return Ranking.query.all()

def get_all_rankings_json():
    rankings = Ranking.query.all()
    if rankings: 
        return [ranking.toJSON() for ranking in rankings]
    return None

def get_rankings_by_ranker(rankerId):
    rankings = Ranking.query.filter_by(rankerId=rankerId)
    if rankings:   
        return[ranking.toJSON() for ranking in rankings]
    return None

def get_rankings_by_image(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId)
    if rankings:
        return [ranking.toJSON() for ranking in rankings]
    return None

def get_ranking_by_actors(rankerId, imageId):
    if Profile.query.get(rankerId) and Image.query.get(imageId):
        return Ranking.query.filter_by(rankerId=rankerId, imageId=imageId).first()
    return None

'''Update operations'''
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
    

#what Use case is this - can be removed
    
def get_calculated_ranking(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId)
    total = 0
    if rankings:
        for ranking in rankings:
            total = total + ranking.score
        if rankings.count() != 0:
            total = total / rankings.count()
        return total
    return None
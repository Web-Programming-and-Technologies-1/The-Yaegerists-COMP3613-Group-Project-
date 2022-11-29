from App.models import Distribution, Profile
from App.database import db
import random
from sqlalchemy.exc import IntegrityError


def distribute():
    #query all profiles
    distributionProfiles= []
    distributionProfiles = Profile.query.all()
    totalProfileNum = len(distributionProfiles)

    #choose 4 random indexes
    rand = random.randint(0, totalProfileNum)
    

#get those profiles by id
#return the profiles

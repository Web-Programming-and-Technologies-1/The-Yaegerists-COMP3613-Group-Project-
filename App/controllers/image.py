from App.models import Image
from App.database import db
from sqlalchemy.exc import IntegrityError

'''Create operations'''
#upload an image to a specific profile
def create_image(profileId):
    new_image = Image(profileId=profileId)
    try:
        db.session.add(new_image)
        db.session.commit()
        return new_image
    except IntegrityError:
        db.session.rollback()
    return None 

'''Read operations'''
def get_image(imageId):
    return Image.query.filter_by(imageId=imageId).first()

def get_image_json(imageId):
    image = get_image(imageId)
    if image:
        return image.toJSON()
    return None

def get_images_by_profileId(profileId):
    return Image.query.filter_by(profileId=profileId)

def get_images_by_profileId_json(profileId):
    images = Image.query.filter_by(profileId=profileId)
    if images:
        return [image.toJSON() for image in images]
    return None

def get_all_images():
    return Image.query.all()

def get_all_images_json():
    images = get_all_images()
    if images:
        return[image.toJSON() for image in images]
    return None

'''Update operations'''
def update_image(imageId,url):
    image = get_image(imageId)
    try:
        if image:
            image.url= url
            db.session.add(image)
            db.session.commit()
            return image
        return None
    except:
        db.session.rollback()
    return None

'''Delete Operations'''
def delete_image(id):
    image = get_image(id)
    try:
        if image:
            db.session.delete(image)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
    return False
from App.models import Image
from App.database import db
from sqlalchemy.exc import IntegrityError

'''Create operations'''
#Upload an image to a specific profile
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
# Return image with the specified Id 
def get_image(imageId):
    return Image.query.filter_by(imageId=imageId).first()

# Gets and return the image with the specified Id in JSON format for None otherwise
def get_image_json(imageId):
    image = get_image(imageId)
    if image:
        return image.toJSON()
    return None

# Return image with the specified profile Id 
def get_images_by_profileId(profileId):
    return Image.query.filter_by(profileId=profileId)

# Get a images with specified profile id 
# return the image if found in JSON format
# return None if image isnt found 
def get_images_by_profileId_json(profileId):
    images = get_images_by_profileId(profileId)
    if images:
        return [image.toJSON() for image in images]
    return None

# Return all images  found
def get_all_images():
    return Image.query.all()

# gets all images and return the images in JSON format or None otherwise
def get_all_images_json():
    images = get_all_images()
    if images:
        return[image.toJSON() for image in images]
    return None

'''Update operations'''
# Get a image based on image ID
# Return none if image not found
# Updates the image details if found
# Returns the updated image or None otherwise
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
# Get a image based n image ID
# Deletes the image if found and return true
# Return false otherwise
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
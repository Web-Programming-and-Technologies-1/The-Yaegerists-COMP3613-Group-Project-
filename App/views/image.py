from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import *

image_views = Blueprint('image_views', __name__, template_folder='../templates')


@image_views.route('/images', methods=['GET'])
def get_image_page():
    images = get_all_images()
    return render_template('images.html', images=images)

@image_views.route('/api/images', methods=['POST'])
def create_image_action():
    data = request.json
    user = get_profile(data['userId'])
    if user:
        image = create_image(data['userId'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/api/images', methods=['GET'])
def get_images_all_action():
    images = get_all_images_json()
    return jsonify(images)

@image_views.route('/api/images/user', methods=['GET'])
def get_images_by_profile_action():
    data = request.json
    images = get_images_by_profileId_json(data['userId'])
    return jsonify(images)

@image_views.route('/api/images/id', methods=['GET'])
def get_images_by_id_action():
    data = request.json
    image = get_image_json(data['id'])
    return jsonify(image)

@image_views.route('/api/images', methods=['DELETE'])
def delete_image_action():
    data = request.json
    if get_image(data['id']):
        delete_image(data['id'])
        return jsonify({"message":"Image Deleted"}) 
    return jsonify({"message":"Image Not Found"}) 
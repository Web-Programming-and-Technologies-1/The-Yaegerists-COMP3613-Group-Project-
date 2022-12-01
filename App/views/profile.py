from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_login import LoginManager, current_user, login_user, login_required, login_manager
from flask_jwt import jwt_required


from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_profile_page():
    users = get_all_profiles()
    return render_template('users.html', users=users)


##not using i believe
@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')


@user_views.route('/api/createUsers', methods=['POST'])
def create_profile_action():
    data = request.json
    user = get_profile_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}) 
    user = create_profile(data['username'], data['email'], data['password'])
    return jsonify({"message":"User Created"}) 


@user_views.route('/api/allProfiles', methods=['GET'])
def get_all_profiles_action():
    users = get_all_profiles_json()
    return jsonify(users)


@user_views.route('/api/users/byid', methods=['GET'])
def get_profile_action():
    data = request.json
    user = get_profile(data['id'])
    if user:
        return user.toJSON() 
    return jsonify({"message":"User Not Found"})

##
# @user_views.route('/api/users/byid', methods=['GET'])
# def get_user_action():
#     id = request.args.get('id')
#     user = get_user(id)
#     if user:
#         return user.toJSON() 
#     return jsonify({"message":"User Not Found"})



@user_views.route('/api/updateUsers', methods=['PUT'])
def update_profile_action():
    data = request.json
    user = update_profile(data['id'], data['username'], data['email'], data['password'])
    if user:
        return jsonify({"message":"User Updated"})
    return jsonify({"message":"User Not Found"})

@user_views.route('/api/deleteUsers', methods=['DELETE'])
def delete_profile_action():
    data = request.json
    if get_profile(data['id']):
        delete_profile(data['id'])
        return jsonify({"message":"User Deleted"}) 
    return jsonify({"message":"User Not Found"}) 


#no controller for this (unsure)
@user_views.route('/api/users/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"})

#left as user because auth uses USER
@user_views.route('/auth', methods=['POST'])
def login_profile_action():
    userData = request.get_json()
    user= authenticate(username = userData['username'], password= userData['password'])
    if user == None:
        return 'ERROR: Wrong username or password!'
    else:
        #login_user(user)
        return 'SUCCESS: User logged in successfully'


# @user_views.route('/api/users/level', methods=['GET'])
# def get_level_action():
#     data = request.json
#     user = get_profile(data['userId'])
#     if user:
#         level = get_level(user.id)
#         return jsonify({"level":f"{level}"})
#     return jsonify({"message":"User Not Found"})

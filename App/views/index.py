from flask import Blueprint, session, redirect, render_template, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_manager, login_required
from flask import Flask, flash
from App.controllers import *
from App.forms import SignUp, LogIn, UploadPicture, EditProfile
import json
# from flask_sqlalchemy_session import current_session


index_views = Blueprint('index_views', __name__,
                        template_folder='../templates')


@index_views.route('/uploadpictures', methods=['GET'])
@login_required
def uploadpictures_page():
    form = UploadPicture()
    return render_template('uploadpictures.html', form=form)


@index_views.route('/uploadpictures', methods=['POST'])
@login_required
def uploadpicturesAction():
    form = UploadPicture()
    data = request.form
    if data == None or data == '':
        flash('Input an Image URL')
        return render_template('uploadpictures.html', form=form)
    if form.validate_on_submit():
        imagedata = create_image(profileId=current_user.profileId, url=data['url'])
        ranking=create_ranking(current_user.profileId,imagedata.imageId,0)
        flash('Uploaded Picture, Check Profile')
        return render_template('uploadpictures.html', form=form)


@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)


@index_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit():  # respond to form submission
    data = request.form
    #   profile = get_profile_by_username(username = data['username'])
    #   if profile and profile.check_password(data['password']): # check credentials USE CONTROLLERS    
    profile = authenticate(username= data['username'], password=data['password'])
    if profile :
        flash('Logged in successfully.') # send message to next page
        login_user(profile, remember=True) # login the user
        profiles=get_all_profiles()
        profiles.remove(profile)
        return render_template('home.html', activeusers=profiles,form=form) # redirect to main page if login successful
  flash('Invalid credentials')
  return render_template('login.html',form=form)


@index_views.route('/signup', methods=['GET'])
def signup_page():
    form = SignUp() # create form object
    return render_template('signup.html', form=form) # pass form object to template
    
@index_views.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newprofile = create_profile(username=data['username'], email=data['email'], password=data['password']) # create user object
    flash('Account Created, Now Login!')# send message
    return render_template('login.html', form= LogIn())# redirect to login page
  flash('Error invalid input! Retry')
  return render_template('signup.html', form = form)

@index_views.route('/', methods=['GET'])
def start_page():
    return render_template('start.html')

@index_views.route('/home', methods=['GET'])
@login_required
def home_page():
    profiles = get_all_profiles()
    for profile in profiles:
        profile.overall_rating = get_total_rating(profile.profileId)         
    profiles=distribute(numProfiles=4,senderId=current_user.profileId)
                                       
    return render_template('home.html', activeusers=profiles)

@index_views.route('/myprofile', methods=['GET'])
@login_required
def myprofile_page():
    ratings = get_calculated_rating(current_user.profileId)
    return render_template('profilepage.html',images=get_images_by_profileId(current_user.profileId) ,profile=current_user, ratings = ratings)

@index_views.route('/toprated', methods=['GET'])
@login_required
def toprated_page():
    profiles = get_top_rated_Profiles()[:4]
    ratings = get_all_ratings()
    return render_template('topratedprofiles.html',profiles=profiles,ratings=ratings)

@index_views.route('/editprofile', methods=['POST','GET'])
@login_required
def editprofile_page():
    form = EditProfile() # create form object
    if request.method == "POST":
      if form.validate_on_submit():
          data = request.form # get data from form submission
          updatedprofile = update_profile(profileId=current_user.profileId,username=data['username'], email=data['email'], password=data['password']) # update user object
          flash('Account Updated!')# send message
      else:
          flash('Error invalid input! Retry')
          return render_template('editprofilepage.html',form=form)# redirect to edit page
    if request.method == "GET":
         return render_template('editprofilepage.html',form=form) # redirect to edit page 

@index_views.route('/otheruserprofile/<id>', methods=['GET', 'POST'])
@login_required
def otheruserprofile_page(id):
    user = get_profile(id)
    rankings=get_all_rankings()
    ###
    ###ProfileRating
    images=get_images_by_profileId(id)
    rating = get_ratings_by_receiver(id)
    average = get_calculated_rating(id)
    average=round(average,2)
    ###
    if request.method == "POST":
        ###ProfileRating
        data = request.form
        rating = create_rating(senderId=current_user.profileId, receiverId=user.profileId, score=data['rating'])
        average = get_calculated_rating(id)
        average=round(average,2)
        ###
        return render_template('otheruserprofile.html',average=average, user=user, images=images, ratings = rating, rankings=rankings)
    
    if request.method == "GET":
        rating = get_ratings_by_receiver(id)
        return render_template('otheruserprofile.html',average=average, user=user, images=images, ratings = rating, rankings=rankings) 
 

@index_views.route('/rankimage/<id>', methods=['GET','POST'])
@login_required
def rankimage_page(id):

       user = get_profile(id)
       images = get_images_by_profileId(id)
       images.rankings=get_rankings_by_ranker(id)
       rating = get_ratings_by_receiver(id)
       average = get_calculated_rating(id)
       average=round(average,2)
       rankings=get_all_rankings()
       images = get_images_by_profileId(id) 
       
       if request.method == "POST":
          data=request.form
          for image,ranking in data.items():
             ranking=create_ranking(current_user.profileId,image,ranking)
             #print("Image ID:",ranking.imageId)
             #print("Rank ID:",ranking.rankingId)
             #print("Rank Score:",ranking.score)
          return render_template('rankingimagepage.html', user=user, images=images, ratings = rating, average=average, rankings=rankings)
       
       if request.method == "GET":
          return render_template('rankingimagepage.html', user=user, images=images, ratings = rating, average=average, rankings=rankings)
       
@index_views.route('/allprofiles', methods=['GET'])
def p_page():
    profiles = get_all_profiles_json
    return profiles

@index_views.route('/deleteImage/<id>', methods=['GET'])
def deleteImage(id):
    ratings = get_calculated_rating(current_user.profileId)
    image = delete_image(id)
    if(image):
        return render_template('profilepage.html',images=get_images_by_profileId(current_user.profileId) ,profile=current_user, ratings = ratings)
    else:
        return render_template('profilepage.html',images=get_images_by_profileId(current_user.profileId) ,profile=current_user, ratings = ratings)
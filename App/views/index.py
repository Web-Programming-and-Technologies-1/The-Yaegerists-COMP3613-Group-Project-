from flask import Blueprint, session, redirect, render_template, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_manager, login_required
from flask import Flask
from App.controllers import *
from App.forms import SignUp, LogIn, UploadPicture
# from flask_sqlalchemy_session import current_session


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/uploadpictures', methods=['GET'])
def uploadpictures_page():
    form = UploadPicture()
    return render_template('uploadpictures.html',form=form)

@index_views.route('/uploadpictures', methods=['POST'])
def uploadpicturesAction():
    form = UploadPicture()
    if form.validate_on_submit():
       data=request.form
       imagedata = create_image(profileId=current_user.profileId,url=data['url'])
       #return render_template('Home.html')   
       return render_template('uploadpictures.html',form=form)  


@index_views.route('/login', methods=['GET'])
def login_page():
    form = LogIn()
    return render_template('login.html', form=form)
    


@index_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      profile = Profile.query.filter_by(username = data['username']).first()
      if profile and profile.check_password(data['password']): # check credentials
        #flash('Logged in successfully.') # send message to next page
        login_user(profile, remember=True) # login the user
        return render_template('home.html', activeusers=get_all_profiles()) # redirect to main page if login successful
  #flash('Invalid credentials')
  return render_template('login.html')


@index_views.route('/signup', methods=['GET'])
def signup_page():
    form = SignUp() # create form object
    return render_template('signup.html', form=form) # pass form object to template
    
@index_views.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newprofile = Profile(username=data['username'], email=data['email'], password=data['password']) # create user object
    db.session.add(newprofile) # save new user
    db.session.commit()
    ##flash('Account Created!')# send message
    return render_template('login.html', form= LogIn())# redirect to login page
  ##flash('Error invalid input!')
  return render_template('signup.html', form = form)

@index_views.route('/', methods=['GET'])
def start_page():
    return render_template('start.html')

@index_views.route('/home', methods=['GET'])
def home_page():
    users = get_all_profiles()
    return render_template('home.html', activeusers=users)

@index_views.route('/myprofile', methods=['GET'])
@login_required
def myprofile_page():
    
    return render_template('profilepage.html',images=get_images_by_profileId(current_user.profileId) ,profile=current_user)

@index_views.route('/toprated', methods=['GET'])
def toprated_page():
    return render_template('topratedprofiles.html')

@index_views.route('/editprofile', methods=['GET'])
def editprofile_page():
    return render_template('editprofilepage.html')  

@index_views.route('/otheruserprofile/<id>', methods=['GET'])
def otheruserprofile_page(id):
    user = get_profile(id)
    userImages = get_images_by_profileId(id)
    return render_template('otheruserprofile.html', user=user, images=userImages)  

@index_views.route('/allprofiles', methods=['GET'])
def p_page():
    profiles = get_all_profiles_json
    return profiles
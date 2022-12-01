from flask import Blueprint, redirect, render_template, request, send_from_directory
from App.controllers import *
from App.forms import SignUp

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/createaccount', methods=['GET'])
def createaccount_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
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
    return render_template('login.html')# redirect to login page
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
def myprofile_page():
    return render_template('profilepage.html')

@index_views.route('/toprated', methods=['GET'])
def toprated_page():
    return render_template('topratedprofiles.html')

@index_views.route('/editprofile', methods=['GET'])
def editprofile_page():
    return render_template('editprofilepage.html')  

@index_views.route('/otheruserprofile/<id>', methods=['GET'])
def otheruserprofile_page(id):
    user = get_profile(id)
    return render_template('otheruserprofile.html', user=user)  

@index_views.route('/allprofiles', methods=['GET'])
def p_page():
    profiles = get_all_profiles_json
    return profiles
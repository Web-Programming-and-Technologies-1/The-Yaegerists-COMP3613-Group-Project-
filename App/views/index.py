from flask import Blueprint, redirect, render_template, request, send_from_directory
from App.controllers import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/createaccount', methods=['GET'])
def createaccount_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


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
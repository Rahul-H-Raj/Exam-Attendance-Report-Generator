########################################################################################
######################          Import packages      ###################################
########################################################################################
import re
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db


auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup():
    if request.method == 'GET':  # If the request is GET, return the signup page and forms
        return render_template('signup.html')
    else:  # If the request is POST, then check if the email doesn't already exist and then save data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Name validation
        if not re.fullmatch(r'^[A-Za-z\s]{1,50}$', name):
            flash('Name must contain only alphabetic characters and spaces, and be between 1 and 50 characters long.')
            return redirect(url_for('auth.signup'))

        # Password validation
        if not re.fullmatch(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            flash('Password must be at least 6 characters long, contain both letters and digits, and include at least one special symbol.')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=email).first()  # If this returns a user, then the email already exists in the database
        if user:  # If a user is found, redirect back to the signup page so the user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # Create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('main.index'))
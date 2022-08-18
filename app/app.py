# create flask app
import numpy as np
import joblib
import os
import pandas as pd
from flask import Flask, render_template, request, session, flash, url_for, redirect, send_file
from map_all import create_map
from models.models import Db, User
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from os import environ
from forms.form import LoginForm, SignupForm, UpdateForm
import gunicorn

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') # this is to solve a bug in heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = environ.get('SECRET_KEY')

Db.init_app(app)

# Load pickle model
path = os.path.join(app.root_path, "static/asset", 'model.pkl')
model = joblib.load(path)

def get_error(e):
    return e.message if hasattr(e, 'message') else str(e)

# Get the currently logged in user
def logged_in_user():
    if 'username' in session and session['username'] != "":
        # Will return None if no such user exists
        return User.query.filter_by( username = session['username'] ).first()
    else:
        return None

# Define homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user=logged_in_user())

# Define about page
@app.route('/about')
def about():
    return render_template('about.html', user=logged_in_user())

# Define prediction page
@app.route('/prediction')
def prediction():
    user = logged_in_user()
    if user == None:
        # redirect back to login page        
        return redirect(url_for('login')) 
    return render_template('prediction.html', user=user)

# Define prediction method
@app.route('/predict', methods=['post'])
def predict():
    countries = { '0': 'USA', '1': 'Belgium', '2': 'Russia', '3': 'Japan'} #session
    activities = { '0': 'Fuel', '1': 'Consumption', '2': 'Energy', '3': 'Own Use'} #session
    session['country'] = countries[request.form['country']] #session
    session['activity'] = activities[request.form['activity']] #session
    features = [x for x in request.form.values()]
    features = pd.DataFrame([features], columns=['country','activity'])
    prediction = np.ravel(model.predict(features))[0].round(1)
    return render_template('prediction.html', prediction= round(prediction), country = features['country'].item(),
                             activity = features['activity'].item(), user=logged_in_user())

# Define maps
@app.route('/map/<year>/<activity_group>', methods=['GET'])
def map(year, activity_group):
    user = logged_in_user()
    if user == None:
        # redirect back to login page        
        return redirect(url_for('login')) 

    if year == '2021':
        return render_template("/prediction_maps/map_" + activity_group + ".html", user=user)

    mapping = create_map(int(year), str(activity_group))

    return render_template("map_all.html",  mapping = mapping, user=user)

# Define graph
@app.route('/graph')
def graph():
    return render_template('graph.html', user=logged_in_user())

# Define flame logo image
@app.route('/image')
def image():
    return send_file('static/asset/logo_flame.jpg')

# Basic code for creat from lab6
# Create a new user (signup)
@app.route( '/user/create', methods=['POST'])
def user_create():
    try:
        # Init form
        form = SignupForm()
        if form.validate_on_submit():
            # Set variables
            username = request.form['username'] 
            password = request.form['password'] 
            verify = request.form['verify']
        
            # Does the user already exist?
            user = User.query.filter_by(username = username).first()
            if user:
                raise LookupError(f'User with username "{username}" already exists! Please choose another username.')
            
            if password != verify:
                raise ValueError(f'Password and password verification don\'t match.')

            # User is unique, so let's create a new one
            user = User(username=username, password=sha256_crypt.hash(password))
            Db.session.add(user)
            Db.session.commit()
            
            # Message Flashing
            # https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/#flashing-with-categories
            flash('Welcome, you are now a registered user!', 'success')
            
            # Redirect to login page
            return redirect(url_for('login'))
        else:
            raise ValueError(f'Invalid characters in username or password.') 
    except Exception as e:
        # Show the error
        flash(get_error(e), 'danger')
        
        # Redirect back to signup page
        return redirect(url_for('signup'))

# Basic code for login from lab6
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():    
    try:
        if request.method == 'POST':
            form = LoginForm()
            # Init & sanitize credentials from form request
            # Sanitition in form.py
            username = request.form['username']
            password = request.form['password']

            if not form.validate_on_submit():
                raise KeyError('Invalid username or password') 
            
            # Get the user user by Db query
            user = User.query.filter_by( username=username ).first()
            if user == None:
                raise KeyError('Invalid username or password')
            
            # Control login validity
            # We have some unhashed passwords in the database, so we may need to fix them
            if user.password == password:
                user.password = sha256_crypt.hash(password) # Password wasn't hashed so we need to do it now
                Db.session.commit() # Save the password hash
                user = User.query.filter_by(username=username).first() # Get the user back again
            
            # Check the password against the hashed version
            if not sha256_crypt.verify(password, user.password):
                raise PermissionError('Invalid username or password')
                
            # Set the logged in user's username in the session   
            session['username'] = username
            
            # Let the user know login was sucessful
            flash(f'{username} is now logged in!', 'success')
            
            # Redirect to index page
            return redirect(url_for('index'))
                
        else: # GET
            # Get the logged in user
            user = logged_in_user()
            
            # Init form
            form = LoginForm()
            
            # Show the login form
            return render_template('login.html', title='Login', form=form, user=user)

    # Any error
    except Exception as e:
        # Show the error
        flash(get_error(e), 'danger')
        
        # Redirect back to login page        
        return redirect(url_for('login')) 

# Basic code for logout from lab6
@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    
    # Redirect back to index page
    return redirect(url_for('index'))

# Basic code for signup from lab6
@app.route('/signup')
def signup():
    # Init form
    form = SignupForm()

    return render_template('signup.html', title='Signup', form=form, user=logged_in_user())

# Define profile page
@app.route('/profile')
def profile():
    user = logged_in_user()
    if user == None:
        # Redirect back to login page        
        return redirect(url_for('login')) 
    return render_template('profile.html', user=user)

# Define update user page
@app.route('/update')
def update():
    user = logged_in_user()
    if user == None:
        # Redirect back to login page        
        return redirect(url_for('login')) 
    # Init form
    form = UpdateForm(obj=user)
    return render_template('update_user.html', form=form, user=user)

@app.route('/user/update/<username>', methods=['POST'])
def user_update(username):
    try:
        user = logged_in_user()

        # Error message
        if user == None:
            raise KeyError('You are not logged in!')

        # Init form
        form = UpdateForm()
        
        # Error message
        if not form.validate_on_submit():
            raise KeyError('Invalid username') 

        # Set variable
        new_username = request.form['username']

        # Error message
        if (username != user.username):
            raise PermissionError('Unauthorized action!')

        # Set new username as username
        user.username = new_username

        # Commit the changes
        Db.session.commit()

        # Set the new username in session
        session['username'] = new_username

        # Redirect to profile page
        return redirect(url_for('profile'))

    except Exception as e:
        # Show the error
        flash(get_error(e), 'danger')
        # Redirect to update page
        return redirect(url_for('update'))

# Basic code for login from lab6
# Delete
@app.route('/user/delete/<username>')
def user_delete(username):
    try:
        # User must be logged in to view user profiles!
        user = logged_in_user()
        if user == None:
            raise KeyError('You are not logged in!')
        
        # We're the only ones who can delete our own user!
        if (username != user.username):
            raise PermissionError('Unauthorized action!')

        # Delete the user
        Db.session.delete(user)
        
        # Commit the changes
        Db.session.commit()
        
        # Our user is dead, so we need to log out!
        return redirect(url_for('logout'))
            
    # Not authorized, go to login page
    except KeyError as ke:
        # Show the error
        flash(get_error(ke), 'danger')
        
        # Redirect to login
        return redirect(url_for('login'))
    
    # Any other error
    except Exception as e:
        # Show the error
        flash(get_error(e), 'danger')
        
        # Redirect back to index page (or referrer)
        last_page = request.referrer if request.referrer else url_for('index')
        return redirect( last_page )   

if __name__ == "__main__":
    app.run(debug=True)

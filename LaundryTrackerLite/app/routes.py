from symbol import decorator
from flask import render_template, redirect, url_for
from flask import request, session
from functools import wraps
from app import app

#allows us require someone is logged in to get to a certain page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function  

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    #do something with request results
    #request.form['username']
    #request.form['password']
    
    #if login valid:
    session['username'] = request.form['username'] #will be used to validate that someone is logged in
    return redirect(url_for('home'))
    #else:
    #say invalid login in some way
    return redirect(url_for('index')) #go back to start page to retry login

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/passwordReset')
def passwordReset():
    return "password reset"

@app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

from symbol import decorator
from functools import wraps

from flask import render_template, redirect, url_for, flash
from flask import request, session

from app import l_app
from app.python import databaseAccess as db
from app.python import emailManagement

#allows us require someone is logged in to get to a certain page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function  



@l_app.route('/')
@l_app.route('/index', methods=['GET','POST'])
@l_app.route('/login', methods=['GET','POST'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html', validLogin=request.args.get('validLogin'))
    else:
        loginValid = db.validLogin(request.form['username'], request.form['password'])
    
        if(loginValid):
            session['username'] = request.form['username'] #will be used for the @login_required flag to validate that someone is logged in
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index', validLogin=False)) #show invalid login error and have them try again



@l_app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))


@l_app.route('/signup', methods=['GET','POST'])
@l_app.route('/signup/<emailTaken>')
@l_app.route('/signup/<emailValid>')
def signup(emailTaken=False, emailValid=True):
    if(request.method == 'GET'):        
        roomList = db.getLaundryRooms()
        return render_template('accountInfo.html', requestType='signup', roomList=roomList, emailTaken=request.args.get('emailTaken'), emailValid=request.args.get('emailValid'))
    else:
        email = request.form['email']
        if(db.checkEmailTaken(email)): #Checks if email is taken
            return redirect(url_for('signup', emailTaken=True))
        else:
            if(emailManagement.isValid(email)) : #Checks if email is valid
                db.registerUser(email, request.form['username'], request.form['password'])
                return redirect(url_for('home')) #redirect to home page
            else:
                return redirect(url_for('signup', emailValid=False))



@l_app.route('/passwordreset')
@login_required
def passwordReset():
    #TODO whole method
    return "password reset"



@l_app.route('/editaccount', methods=['GET','POST'])
@l_app.route('/editaccount/<emailTaken>')
@l_app.route('/editaccount/<emailValid>')
@login_required
def editAccount(emailTaken=False, emailValid=True):
    if(request.method == 'GET'):
        roomList = db.getLaundryRooms()

        currentUsername = session['username']
        userData = db.getUserData(currentUsername)

        return render_template('accountInfo.html', requestType='edit', userData=userData, roomList=roomList, emailTaken=request.args.get('emailTaken'), emailValid=request.args.get('emailValid'))
    else:
        oldEmail = request.form['oldEmail']
        newEmail = request.form['email']
        #If email changed, validate new email
        if(oldEmail != newEmail):
            if(db.checkEmailTaken(newEmail)): #Checks if email is taken
                return redirect(url_for('editAccount', emailTaken=True))
            if(not emailManagement.isValid(newEmail)): #Checks if email is invalid
                return redirect(url_for('editAccount', emailValid=False))
        #If it makes it to here, email is both available and valid
        #Save new details to database
        db.updateUser(request.form['oldEmail'], request.form['email'], request.form['username'], request.form['password'])
        #update session information
        session['username'] = request.form['username']

        return redirect(url_for('home')) #redirect to home page
    


@l_app.route('/home')
@login_required
def home():
    #TODO pull actual data from database and format better based on how database works

    # userMachines represents the machines that a user currently has checked out (is using)
    # allMachines shows all machines and their status
    # laundryRoomList contains the names of the laundry rooms
    userMachines = []
    allMachines = []
    roomList = []
    
    return render_template('home.html', userMachines=userMachines, allMachines=allMachines, laundryRoomList=roomList)

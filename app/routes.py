from symbol import decorator
from functools import wraps

from flask import render_template, redirect, url_for, flash
from flask import request, session

from app import l_app
from app import mysql
from app.python import databaseAccess as db

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
def index(validLogin=True):
    if(request.method == 'GET'):
        return render_template('index.html', validLogin=validLogin)
    else:
        loginValid = db.validLogin(request.form['username'], request.form['password'])
    
        if(loginValid):
            session['username'] = request.form['username'] #will be used for the @login_required flag to validate that someone is logged in
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index', validLogin=False)) #show invalid login error and have then try again



@l_app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))


@l_app.route('/signup', methods=['GET','POST'])
@l_app.route('/signup/<emailTaken>')
def signup(emailTaken=False):
    if(request.method == 'GET'):
        #TODO pull list of laundry rooms from database
        roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']

        return render_template('accountInfo.html', requestType='signup', roomList=roomList, emailTaken=emailTaken)
    else:
        # if the user tries to redirect with a link, send them back to the
        # original page that they were at.

        #TODO save new account to database
        email = request.form['email']
        username = request.form['username']
        request.form['password']

        # connect to the database with cursor
        cursor = mysql.connection.cursor()

        # check the database to see if the email already exists
        cursor.execute( '''SELECT * FROM MachineUser WHERE email="%s"''' % str(email) )
        temp = cursor.fetchall()

        if (len(temp) != 0): 
            return redirect(url_for('signup', emailTaken=True))

        # if the email doesn't exist, validate the email
        # TODO create, then pull this from a supplementary python script used for
        # methods that help the routes file in the backend
        
        # close database connection
        cursor.close()

        return redirect(url_for('home')) #redirect to home page



@l_app.route('/passwordreset')
@login_required
def passwordReset():
    #TODO whole method
    return "password reset"



@l_app.route('/editaccount', methods=['GET','POST'])
@login_required
def editAccount():
    if(request.method == 'GET'):
        #TODO pull list of laundry rooms from database
        roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']

        #TODO get user data of person currently logged in
        userData = {'email':'user@gmail.com','username':'testUser','preferredRoom':'154W Wads (First floor west)'}

        return render_template('accountInfo.html', requestType='edit', userData=userData, roomList=roomList)
    else:
        #TODO save new details to database
        #request.form['oldEmail']
        #request.form['email']
        #request.form['username']
        #request.form['password']
        #request.form['passwordConfirm']

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

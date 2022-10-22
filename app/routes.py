from functools import wraps

from flask import render_template, redirect, url_for
from flask import request, session

from app import l_app
from app.python import databaseAccess as db
from app.python import emailManagement

from app import mysql
import app.python.signup_helper as signupHelper


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


@l_app.route('/signup', methods=['GET', 'POST'])
@l_app.route('/signup/<emailTaken>', methods=['GET', 'POST'])
def signup(emailTaken=False):
    #TODO pull list of laundry rooms from database

    if (request.method == 'GET'):
        roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']
        return render_template('accountInfo.html', requestType='signup', roomList=roomList, emailTaken=emailTaken)

    if (request.method == 'POST'):
        # get the email and username from the form
        email = request.form['email']
        username = request.form['username']

        # connect to the database with cursor
        # TODO use ACID transactions to help with concurrent queries
        #   - set transaction isolation level serializable
        cursor = mysql.connection.cursor()

        # check the database to see if the email already exists
        cursor.execute( '''SELECT * FROM MachineUser WHERE email=%s''', (str(email),) )
        if (len(cursor.fetchall()) != 0): 
            return redirect(url_for('signup', emailTaken=True))

        # First, salt and hash the password and store all of the info in the database
        # the password is only now pulled from the form
        pass_hash = signupHelper.generateHashAndSalt(str(request.form['password']))

        cursor.execute( ('''INSERT INTO MachineUser VALUES (%s, %s, %s, %s)'''), 
                        (str(email), str(username), str(pass_hash[0]), str(pass_hash[1])) )

        # close the database connection and validate the email
        cursor.close()
        mysql.connection.commit()
        return redirect(url_for('verifyEmail', email=str(email), count=1))
    

@l_app.route('/verifyemail', methods = ['GET', 'POST'])
@l_app.route('/verifyemail/<email>/<count>', methods = ['GET', 'POST'])
def verifyEmail(email, count):
    
    # if we are sending a GET
    if (request.method == 'GET'):
        verification_code = signupHelper.sendSignupEmail(email)
        session['verification_code'] = verification_code
        return render_template('email_verifier.html', email=email, count=count)

    if (request.method == 'POST'):
        # get the current number of attempts
        attempt_count = request.form['count']

        # if the correct code is input
        if (session.get('verification_code') == str(request.form['codeInput'])):
            return redirect(url_for('index'))

        # if we still haven't passed 3 attempts let another attempt happen
        _count = int(attempt_count)
        if (_count <= 3):
            _count += 1
            return redirect(url_for('verifyEmail', email=email, count=_count))

            # If unsuccessful, open a connection to the database and remove the tuple for "email"
        # Then redirect to the sign up page
        cursor = mysql.connection.cursor()
        cursor.execute( '''DELETE FROM MachineUser WHERE email=%s''', (str(email),) )
        cursor.close()
        mysql.connection.commit()
        return redirect(url_for('signup'))



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
    userMachines = db.getUserMachines(session['username'])
    allMachines = db.getAllMachines()
    roomList = db.getLaundryRooms()
    
    return render_template('home.html', userMachines=userMachines, allMachines=allMachines, laundryRoomList=roomList)

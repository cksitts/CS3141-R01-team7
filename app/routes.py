from crypt import methods
from functools import wraps

from flask import render_template, redirect, url_for, abort
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
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(session.get('admin') == 0):
            abort(403) #go to unauthorized error page
        return f(*args, **kwargs)
    return decorated_function  

#Error handling
@l_app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
@l_app.errorhandler(500)
def internal_error(error):
    return render_template('error500.html'), 500
@l_app.errorhandler(403)
def forbidden_page(error):
    return render_template('error403.html'), 403
@l_app.errorhandler(418)
def forbidden_page(error):
    return render_template('error418.html'), 418


@l_app.route('/')
@l_app.route('/index', methods=['GET','POST'])
@l_app.route('/login', methods=['GET','POST'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html', validLogin=request.args.get('validLogin'))
    else:
        username = request.form['username']
        loginValid = db.validLogin(username, request.form['password'])
    
        if(loginValid):
            session['username'] = username # will be used for the @login_required flag to validate that someone is logged in
            session['admin'] = db.isAdmin(username) #1 if admin, 0 otherwise


            return redirect(url_for('home'))
        else:
            return redirect(url_for('index', validLogin=False)) #show invalid login error and have them try again
            

@l_app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))


@l_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'GET'):
        roomList = db.getLaundryRooms()
        return render_template('accountInfo.html',  requestType='signup', 
                                                    roomList=roomList, 
                                                    emailTaken=request.args.get('emailTaken', default=False), 
                                                    emailValid=request.args.get('emailValid', default=True))
    else:
        email = request.form['email'] # get the email from the form
        if(db.checkEmailTaken(email)): #Checks if email is taken
            return redirect(url_for('signup', emailTaken=True))
        else:
            # if the email is not taken then generate a verification code, email the user, and move on to email verification
            session['verificationCode'] = emailManagement.sendSignupEmail(email)

            # store the current user in the session dict for later use (hopefully)
            storedUser = request.form
            session['storedUser'] = storedUser
            session['inputCount'] = 0

            return redirect(url_for('verify', validCode=True, inputCount=session['inputCount']))

@l_app.route('/verify', methods=['GET', 'POST'])
@l_app.route('/verify/<validCode>/<inputCount>', methods=['GET'])
def verify(validCode=True, inputCount=0):

    if (request.method == 'GET'):
        return render_template('verifyEmail.html', validCode=validCode, inputCount=session['inputCount'])
    else:
        verificationCode = request.form['codeInput']
        if(verificationCode == session['verificationCode']):
            # successful verification
            # db.verifyUser(verificationCode) #approves the user to be added to the database

            # register the user in the database
            db.registerUser(session['storedUser'])

            session.pop('verificationCode') #clears the used session data
            session.pop('storedUser')
            session.pop('inputCount')

            # redirect to the login page; users should attempt a login after signing up to verify data integrity
            return redirect(url_for('index'))
        else:
            # if the user has input more than 5 times, reject the validation attempt
            if (session['inputCount'] < 3):
                session['inputCount'] += 1
                return redirect(url_for('verify', validCode=False, inputCount=session['inputCount']))
            else:
                # unsuccessful
                return redirect(url_for('signup'))
            



@l_app.route('/passwordreset')
@login_required
def passwordReset():
    #TODO whole method (return 501 means not implemented)
    return render_template('passwordReset.html'), 501


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
    

@l_app.route('/deleteaccount', methods=['POST'])
@login_required
def deleteAccount():
    db.deleteUser(request.form['email'])
    return redirect(url_for('home')) #redirect to home page


@l_app.route('/home')
@login_required
def home():
    # userMachines represents the machines that a user currently has checked out (is using)
    # allMachines shows all machines and their status
    # laundryRoomList contains the names of the laundry rooms
    userMachines = db.getUserMachines(session['username'])
    allMachines = db.getAllMachines()
    roomList = db.getLaundryRooms()
    preferredRoom = db.getUserData(session['username'])['preferredRoom']
    
    return render_template('home.html', userMachines=userMachines, allMachines=allMachines, laundryRoomList=roomList, preferredRoom=preferredRoom)


@l_app.route('/checkout/<machineId>')
@login_required
def checkout(machineId):
    if(db.checkout(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@l_app.route('/checkin/<machineId>')
@login_required
def checkin(machineId):
    if(db.checkin(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@l_app.route('/addmachines', methods=['GET','POST'])
@admin_only
def addMachines():
    if(request.method == 'GET'):
        return render_template('addMachines.html', locationList=db.getLocations(), successMessage=request.args.get('successMessage', default=False), machineAlreadyExists = request.args.get('machineAlreadyExists', default=False))
    else:
        id = "{roomNum}_{building}_{machineNum}".format(roomNum=request.form['roomNumber'], building=request.form['building'], machineNum=request.form['machineNum'])
        location = request.form['location']
        type = request.form['machineType']
        if(db.addMachine(id, location, type) == 0):
            #successfully added
            return redirect(url_for('addMachines', successMessage="{} added successfully".format(id)))
        else:
            #not successful
            return redirect(url_for('addMachines', machineAlreadyExists=True))


@l_app.route('/teapot')
def teapotPage():
    abort(418) 
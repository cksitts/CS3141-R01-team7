from crypt import methods
from functools import wraps

from flask import render_template, redirect, url_for, abort
from flask import request, session, current_app

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
@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
@current_app.errorhandler(500)
def internal_error(error):
    return render_template('error500.html'), 500
@current_app.errorhandler(403)
def forbidden_page(error):
    return render_template('error403.html'), 403
@current_app.errorhandler(418)
def im_a_teapot(error):
    return render_template('error418.html'), 418


@current_app.route('/')
@current_app.route('/index', methods=['GET','POST'])
@current_app.route('/login', methods=['GET','POST'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html', validLogin=request.args.get('validLogin'))
    else:
        username = request.form['username']
        loginValid = db.validLogin(username, request.form['password'])
    
        if(loginValid):
            # will be used for the @login_required flag to validate that someone is logged in
            # if the username is an email, still store the username associated with that email (usernames cannot contain '@')
            session['username'] = username if '@' not in username else db.getUsernameFromEmail(username)
            session['admin'] = db.isAdmin(username) #1 if admin, 0 otherwise


            return redirect(url_for('home'))
        else:
            return redirect(url_for('index', validLogin=False)) #show invalid login error and have them try again
            

@current_app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))


@current_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'GET'):
        roomList = db.getLaundryRooms()
        return render_template('accountInfo.html',  requestType='signup', 
                                                    roomList=roomList, 
                                                    status_code=request.args.get('status_code', default=0), 
                                                    emailValid=request.args.get('emailValid', default=True))
    else:
        email = request.form['email'] # get the email from the form
        username = request.form['username']
        status_code = db.checkEmailAndUsernameTaken(email, username) #Checks if email is taken

        if (status_code != 0):
            return redirect(url_for('signup', status_code=status_code))
        else:
            # if the email is not taken then generate a verification code, email the user, and move on to email verification
            session['verificationCode'] = emailManagement.sendSignupEmail(email)

            # store the current user in the session dict for later use (hopefully)
            storedUser = request.form
            session['storedUser'] = storedUser
            session['inputCount'] = 1
            session['validCode'] = True

            return redirect(url_for('verify'))

@current_app.route('/verify', methods=['GET', 'POST'])
def verify():
    if (request.method == 'GET'):
        return render_template('verifyEmail.html',  validCode=session['validCode'],
                                                    inputCount=session['inputCount'])
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
            



@current_app.route('/passwordreset')
@login_required
def passwordReset():
    #TODO whole method (return 501 means not implemented)
    return render_template('passwordReset.html'), 501


@current_app.route('/editaccount', methods=['GET','POST'])
@login_required
def editAccount():
    currentUsername = session['username']
    userData = db.getUserData(currentUsername)
    if(request.method == 'GET'):
        roomList = db.getLaundryRooms()

        return render_template('accountInfo.html', 
                                requestType='edit', 
                                userData=userData, 
                                roomList=roomList, 
                                status_code=request.args.get('status_code', default=False), 
                                emailValid=request.args.get('emailValid', default=True))
    else:
        oldEmail = request.form['oldEmail']
        newEmail = request.form['email']

        #If email changed, validate new email
        # if(not emailManagement.isValid(newEmail)): #Checks if email is invalid
        #     return redirect(url_for('editAccount', emailValid=False))

        #If it makes it to here, email is both available and valid
        #Save new details to database
        status_code = db.updateUser(oldEmail, newEmail, userData['username'], request.form['username'], request.form['password'])
        if (status_code != 0):
            return redirect(url_for('editAccount', status_code=status_code))

        # update session information
        session['username'] = request.form['username']

        return redirect(url_for('home')) #redirect to home page
    

@current_app.route('/deleteaccount', methods=['POST'])
@login_required
def deleteAccount():
    db.deleteUser(request.form['email'])
    return redirect(url_for('home')) #redirect to home page


@current_app.route('/home')
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


@current_app.route('/checkout/<machineId>')
@login_required
def checkout(machineId):
    if(db.checkout(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@current_app.route('/checkin/<machineId>')
@login_required
def checkin(machineId):
    if(db.checkin(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@current_app.route('/addmachines', methods=['GET','POST'])
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


@current_app.route('/teapot')
def teapotPage():
    abort(418)

@current_app.route('/about')
def aboutPage():
    return render_template('about.html')
@current_app.route('/help')
def helpPage():
    return render_template('help.html')
@current_app.route('/reportIssue')
def reportIssuePage():
    return render_template('reportIssue.html')
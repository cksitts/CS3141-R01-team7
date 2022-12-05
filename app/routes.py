from crypt import methods
from functools import wraps

from flask import render_template, redirect, url_for, abort, Blueprint
from flask import request, session, current_app

from app.python import databaseAccess as db
from app.python import emailManagement

# DEFINE BLUEPRINTS
error = Blueprint('error', __name__, template_folder='/templates/errors')
footer = Blueprint('footer', __name__, template_folder='/templates/footer')
user = Blueprint('user', __name__, template_folder='/templates/user')
main = Blueprint('main', __name__, template_folder='/templates/main')


#allows us require someone is logged in to get to a certain page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function  
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(session.get('admin') == 0 or session.get('admin') == None):
            abort(403) #go to unauthorized error page
        return f(*args, **kwargs)
    return decorated_function  

#Error handling
@error.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/error404.html'), 404
@error.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/error500.html'), 500
@error.app_errorhandler(403)
def forbidden_page(error):
    return render_template('errors/error403.html'), 403
@error.app_errorhandler(418)
def im_a_teapot(error):
    return render_template('errors/error418.html'), 418


@main.route('/')
@main.route('/index', methods=['GET','POST'])
@main.route('/login', methods=['GET','POST'])
def index():
    if(request.method == 'GET'):
        return render_template('user/index.html', validLogin=request.args.get('validLogin'))
    else:
        username = request.form['username']
        loginValid = db.validLogin(username, request.form['password'])
    
        if(loginValid):
            # will be used for the @login_required flag to validate that someone is logged in
            # if the username is an email, still store the username associated with that email (usernames cannot contain '@')
            session['username'] = username if '@' not in username else db.getUsernameFromEmail(username)
            session['admin'] = db.isAdmin(username) #1 if admin, 0 otherwise


            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('main.index', validLogin=False)) #show invalid login error and have them try again
            

@user.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('main.index'))


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'GET'):
        roomList = db.getLaundryRooms()
        return render_template('user/accountInfo.html',  requestType='signup', 
                                                    roomList=roomList, 
                                                    status_code=request.args.get('status_code', default=0), 
                                                    emailValid=request.args.get('emailValid', default=True))
    else:
        email = request.form['email'] # get the email from the form
        username = request.form['username']
        status_code = db.checkEmailAndUsernameTaken(email, username) #Checks if email is taken

        if (status_code != 0):
            return redirect(url_for('user.signup', status_code=status_code))
        else:
            # if the email is not taken then generate a verification code, email the user, and move on to email verification
            session['verificationCode'] = emailManagement.sendSignupEmail(email)

            # store the current user in the session dict for later use (hopefully)
            storedUser = request.form
            session['storedUser'] = storedUser
            session['inputCount'] = 1
            session['validCode'] = True
            session['resetPass'] = False

            return redirect(url_for('user.verify'))

@user.route('/verify', methods=['GET', 'POST'])
def verify():
    if (request.method == 'GET'):
        return render_template('user/verifyEmail.html', validCode=session['validCode'],
                                                        inputCount=session['inputCount'])
    else:
        verificationCode = request.form['codeInput']
        if(verificationCode == session['verificationCode']):
            # successful verification

            # if signing up: register the user in the database
            if (not session['resetPass']):
                db.registerUser(session['storedUser'])
                session.pop('storedUser')
            else:
                # if we are verifying a password-reset 
                db.changePassword(session['username'], session['password'])
                session.pop('username')
                session.pop('password')
            
            session.pop('verificationCode')
            session.pop('inputCount')
            session.pop('validCode')
            session.pop('resetPass')

            # redirect to the login page; users should attempt a login after signing up to verify data integrity
            return redirect(url_for('main.index'))
        else:
            # if the user has input more than 5 times, reject the validation attempt
            if (session['inputCount'] < 3):
                session['inputCount'] += 1
                session['validCode'] = False
                return redirect(url_for('user.verify', validCode=False, inputCount=session['inputCount']))
            else:
                # unsuccessful
                reset = session['resetPass']
                session.pop('resetPass')
                session.pop('verificationCode')
                session.pop('inputCount')
                session.pop('validCode')
                return redirect(url_for('user.signup')) if not reset else redirect(url_for('main.index'))
            

@user.route('/passwordreset', methods=['GET', 'POST'])
def passwordReset():
    if (request.method == 'GET'):
        return render_template('user/passwordReset.html', validLogin=request.args.get('validLogin', default=True))
    else:
        session['username'] = request.form['usernameInput']
        session['password'] = request.form['passwordInput']
        
        user = db.getUserData(session['username'])
        if (user != None):
            # user exists and so can reset password if verification passes
            session['resetPass'] = True
            session['verificationCode'] = emailManagement.sendPasswordResetEmail(user['email'])
            session['inputCount'] = 0
            session['validCode'] = True
            return redirect( url_for('user.verify', validCode=True, inputCount=session['inputCount']) )
        else:
            # failed: user does not exist
            session.pop('username')
            return redirect( url_for('user.passwordReset', validLogin=(user != None)) )


@user.route('/editaccount', methods=['GET','POST'])
@login_required
def editAccount():
    currentUsername = session['username']
    userData = db.getUserData(currentUsername)
    if(request.method == 'GET'):
        roomList = db.getLaundryRooms()

        return render_template('user/accountInfo.html', 
                                requestType='edit', 
                                userData=userData, 
                                roomList=roomList, 
                                status_code=request.args.get('status_code', default=False), 
                                emailValid=request.args.get('emailValid', default=True))
    else:
        oldEmail = request.form['oldEmail']
        newEmail = request.form['email']

        #Save new details to database
        status_code = db.updateUser(oldEmail, newEmail, userData['username'], request.form['username'], request.form['password'])
        if (status_code != 0):
            return redirect(url_for('user.editAccount', status_code=status_code))

        # update session information
        session['username'] = request.form['username']

        return redirect(url_for('main.home')) #redirect to home page
    

@user.route('/deleteaccount', methods=['POST'])
@login_required
def deleteAccount():
    db.deleteUser(request.form['email'])
    return redirect(url_for('main.index')) # redirect to login page

@main.route('/home')
@login_required
def home():
    # userMachines represents the machines that a user currently has checked out (is using)
    # allMachines shows all machines and their status
    # laundryRoomList contains the names of the laundry rooms
    userMachines = db.getUserMachines(session['username'])
    allMachines = db.getAllMachines()
    roomList = db.getLaundryRooms()
    preferredRoom = db.getUserData(session['username'])['preferredRoom']
    
    return render_template('main/home.html', userMachines=userMachines, allMachines=allMachines, laundryRoomList=roomList, preferredRoom=preferredRoom)


@main.route('/checkout/<machineId>')
@login_required
def checkout(machineId):
    if(db.checkout(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('main.home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@main.route('/checkin/<machineId>')
@login_required
def checkin(machineId):
    if(db.checkin(machineId, session['username']) == 0):
        #successful
        return redirect(url_for('main.home')) #redirect to home page
    else:
        #unsuccessful
        abort(500)


@main.route('/addmachines', methods=['GET','POST'])
@admin_only
def addMachines():
    if(request.method == 'GET'):
        return render_template('main/addMachines.html', locationList=db.getLocations(), successMessage=request.args.get('successMessage', default=False), machineAlreadyExists = request.args.get('machineAlreadyExists', default=False))
    else:
        id = "{roomNum}_{building}_{machineNum}".format(roomNum=request.form['roomNumber'], building=request.form['building'], machineNum=request.form['machineNum'])
        location = request.form['location']
        type = request.form['machineType']
        if(db.addMachine(id, location, type) == 0):
            #successfully added
            return redirect(url_for('main.addMachines', successMessage="{} added successfully".format(id)))
        else:
            #not successful
            return redirect(url_for('main.addMachines', machineAlreadyExists=True))


@error.route('/teapot')
def teapotPage():
    abort(418)

@footer.route('/about')
def aboutPage():
    return render_template('footer/about.html')

@footer.route('/help')
def helpPage():
    return render_template('footer/help.html')
@footer.route('/reportIssue')

def reportIssuePage():
    return render_template('footer/reportIssue.html')
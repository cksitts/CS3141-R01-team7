from symbol import decorator
from functools import wraps

from flask import render_template, redirect, url_for
from flask import request, session

from app import l_app
from app import mysql

#allows us require someone is logged in to get to a certain page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function  



@l_app.route('/')
@l_app.route('/index')
@l_app.route('/index/<validLogin>')
def index(validLogin=True):
    return render_template('index.html', validLogin=validLogin)



@l_app.route('/login', methods=['GET','POST'])
def login():
    #TODO check if login valid:
    #request.form['username']
    #request.form['password']
    loginValid = True
    
    if(loginValid):
        session['username'] = request.form['username'] #will be used to validate that someone is logged in
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index', validLogin=False)) #show invalid login error and have then try again



@l_app.route('/logout')
@login_required
def logout():
    session.pop('username', default=None)
    return redirect(url_for('index'))



@l_app.route('/signup')
def signup():
    #TODO pull list of laundry rooms from database
    roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']

    return render_template('accountInfo.html', requestType='signup', roomList=roomList)



@l_app.route('/signup/request', methods=['GET','POST'])
def signupRequest():
    #TODO save new account to database
    #request.form['email']
    #request.form['username']
    #request.form['password']
    #request.form['passwordConfirm']

    return redirect(url_for('home')) #redirect to home page



@l_app.route('/passwordreset')
@login_required
def passwordReset():
    #TODO whole method
    return "password reset"



@l_app.route('/editaccount')
@login_required
def editAccount():
    #TODO pull list of laundry rooms from database
    roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']

    #TODO get user data of person currently logged in
    userData = {'email':'user@gmail.com','username':'testUser','preferredRoom':'154W Wads (First floor west)'}

    return render_template('accountInfo.html', requestType='edit', userData=userData, roomList=roomList)



@l_app.route('/editaccount/request', methods=['GET','POST']) 
@login_required  
def editAccountRequest():
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

    # connect to the sql server so that we can run queries
    cursor = mysql.connection.cursor()

    # execute a query to insert data into the database
    # note: if this executes correctly, you will only be able to successfully run it once
    # that's just for testing purposes obviously this won't be a problem in the final application
    cursor.execute( ''' insert into MachineUser values ("asdf", "asdf", "FFFFFFFFF", "XYZXYZ") ''' )
    cursor.execute( ''' select pass_hash from MachineUser where email="asdf" ''')

    output = cursor.fetchall()

    # commit the changes to the sql server
    mysql.connection.commit()

    # close the connection to the cursor
    cursor.close()

    #TODO pull actual data from database and format better based on how database works
    allMachines = [
            {
                'code':'134EWH1',
                'location':'134E Wads (First floor east)',
                'number':1,
                'type':'washer',
                'available':False,
                'time-remaining':30
            }]

    return str(output)

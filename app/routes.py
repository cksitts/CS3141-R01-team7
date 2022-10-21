from symbol import decorator
from flask import render_template, redirect, url_for
from flask import request, session
from functools import wraps
from app import l_app
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
    #TODO pull actual data from database and format better based on how database works
    allMachines = [
            {
                'code':'134EWH1',
                'location':'134E Wads (First floor east)',
                'number':1,
                'type':'washer',
                'available':False,
                'time-remaining':30
            },
            {
                'code':'134EWH2',
                'location':'134E Wads (First floor east)',
                'number':2,
                'type':'washer',
                'available':False,
                'time-remaining':20
            },
            {
                'code':'134EWH3',
                'location':'134E Wads (First floor east)',
                'number':1,
                'type':'dryer',
                'available':False,
                'time-remaining':60
            },
            {
                'code':'154WWH1',
                'location':'154W Wads (First floor west)',
                'number':1,
                'type':'washer',
                'available':True,
                'time-remaining':0
            },
            {
                'code':'154WWH2',
                'location':'154W Wads (First floor west)',
                'number':2,
                'type':'washer',
                'available':True,
                'time-remaining':0
            },
            {
                'code':'154WWH3',
                'location':'154W Wads (First floor west)',
                'number':3,
                'type':'washer',
                'available':False,
                'time-remaining':10
            }
    ]
    userMachines = ['134EWH1','134EWH2','154WWH2']
    
    #TODO pull list of laundry rooms from database
    roomList = ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']
    
    return render_template('home.html', userMachines=userMachines, allMachines=allMachines, laundryRoomList=roomList)

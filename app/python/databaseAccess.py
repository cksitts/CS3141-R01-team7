from app import mysql

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    #TODO 
    # check if username is in database
    # check if password matches username
    return True


# Returns a list of laundry rooms from the database
def getLaundryRooms():
    return ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']


# Checks if an email is already being used in the database
def checkEmailTaken(email):
    cursor = mysql.connection.cursor()

    # check the database to see if the email already exists
    cursor.execute( '''SELECT * FROM MachineUser WHERE email="%s"''' % str(email) )
    temp = cursor.fetchall()

    # close database connection
    cursor.close()

    if (len(temp) != 0): 
        return True
    else:
        return False


# Registers a new user in the database
# Returns 0 if successful, otherwise 1
def registerUser(email, username, password):
    #TODO register user in the database
    return 0


# Registers a new user in the database
# Returns 0 if successful, otherwise 1
def updateUser(oldEmail, newEmail, username, password):
    #TODO update user data based on oldEmail (email may or may not change)
    return 0


# Returns the data for a user based on username
def getUserData(username):
    #TODO get user data based on username
    return {'email':'user@gmail.com','username':'testUser','preferredRoom':'154W Wads (First floor west)'}
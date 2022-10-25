from app import mysql
from app.python import helper

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    #TODO 
    # check if username is in database
    # check if password matches username
    return False


# Returns a list of laundry rooms from the database
def getLaundryRooms():
    #TODO
    return ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']


# Returns a list of all machines and their data from the database
def getAllMachines():
    #TODO
    return []


# Checks if an email is already being used in the database
def checkEmailTaken(email):
     # connect to the database with cursor
    # TODO use ACID transactions to help with concurrent queries
    #   - set transaction isolation level serializable
    cursor = mysql.connection.cursor()

    # check the database to see if the email already exists
    cursor.execute( '''SELECT * FROM MachineUser WHERE email=%s''', (str(email),) )
    if (len(cursor.fetchall()) != 0): 
        # close the database connection
        cursor.close()
        return True
    else:
        # close the database connection
        cursor.close()
        return False


# Registers a new user in the database
# Returns 0 if successful, otherwise 1
def registerUser(form):
    # connect to the database with cursor
    # TODO use ACID transactions to help with concurrent queries
    #   - set transaction isolation level serializable
    cursor = mysql.connection.cursor()

    # First, salt and hash the password and store all of the info in the database
    # the password is only now pulled from the form
    pass_hash = helper.generateHashAndSalt(str(form['password']))

    cursor.execute( ('''INSERT INTO MachineUser VALUES (%s, %s, %s, %s)'''), 
                    (str(form['email']), str(form['username']), str(pass_hash[0]), str(pass_hash[1])) )

    # close the database connection
    cursor.close()
    mysql.connection.commit()

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


# Returns a list of machines that the user has checked out
def getUserMachines(username):
    #TODO
    return[]
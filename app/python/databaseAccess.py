from app import mysql
from app.python import helper

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    cursor = mysql.connection.cursor()

    # get this user's data if it exists
    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (str(username),))
    tuple = cursor.fetchone()
    if len(tuple) != 0:
        # username is in the database so get the password hash
        t_hash = tuple[2]                                           # get the password hash stored in the
        hash = helper.getHash( str(password + tuple[3]) )           # generate a hash to compare
        return hash == t_hash                                       # return true if the generated hash equals the stored hash

    return False


# Returns a list of laundry rooms from the database
def getLaundryRooms():
    #TODO
    return ['G23E Wads (Ground floor east)','134E Wads (First floor east)','154W Wads (First floor west)']


# Returns a list of all machines and their data from the database
# TODO machines that are specifically in use (we will just have to decide how we want to get this data)
#   - in use machines is a subset of all machines
def getAllMachines():
    machines = []                           # array holds all machines

    cursor = mysql.connection.cursor()      # open database connection

    # all machines, doesn't show whether or not they are in use.
    cursor.execute( ''' SELECT * FROM Machine ''' )
    all_machine_tuples = cursor.fetchall()

    for t in all_machine_tuples:
        machines.append( {'machine-id' : t[0], 'email' : t[1], 'username' : t[2], 'time-remaining' : 0 } )

    cursor.close()

    # return the list as an array
    return machines

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
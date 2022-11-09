from app import mysql
from app.python import helper
from app.python.constant import VERIFICATION_TIMEOUT

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    # get this user's data if it exists
    cursor = mysql.connection.cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (str(username),))

    tuple = cursor.fetchone()
    if tuple != None:
        # username is in the database so get the password hash
        t_hash = tuple[3]                                           # get the password hash stored in the
        hash = helper.getHash( str(password + tuple[4]) )           # generate a hash to compare
        cursor.execute(''' COMMIT ''')                              # end and commit the transaction
        return hash == t_hash                                       # return true if the generated hash equals the stored hash

    cursor.execute(''' ROLLBACK ''')
    return False


# Returns a list of laundry rooms from the database
def getLaundryRooms():
    rooms = []                           # array holds room strings

    cursor = mysql.connection.cursor()      # open database connection

    # all distinct room numbers and their building
    cursor.execute( '''     SELECT DISTINCT
	                            SUBSTRING_INDEX(machine_id, '_', 1) as Room,
                                SUBSTRING_INDEX(SUBSTRING_INDEX(machine_id, '_', -2), '_' ,1) as Building
                            FROM Machine
                            WHERE NOT machine_id='';
                    ''' )
    all_room_tuples = cursor.fetchall()

    for t in all_room_tuples:
        room = t[0]
        if t[1] == "WH":
            building = "Wads"
        elif t[1] == "MH":
            building = "McNair"
        elif t[1] == "DHH":
            building = "DHH"
        else:
            building = ""

        rooms.append(room + " " + building)

    # all distinct locations
    cursor.execute( ''' SELECT DISTINCT location FROM Machine WHERE NOT location='' ''' )
    all_room_tuples = cursor.fetchall()

    i = 0
    for t in all_room_tuples:
        rooms[i] = rooms[i] + " (" + t[0] + ")"
        i += 1

    cursor.close()

    # return the list as an array
    return rooms


# Returns a list of all machines and their data from the database
#   - in use machines is a subset of all machines
def getAllMachines():
    machines = []                           # array holds all machines

    cursor = mysql.connection.cursor()      # open database connection

    # all machines, doesn't show whether or not they are in use.
    cursor.execute( '''     SELECT  machine_id, machine_type, location, ifnull(username, 'None') as username, 
                                    ifnull(time_started, 0) as time_started, ifnull(available, 1) as available
                            FROM Machine NATURAL LEFT JOIN (
                                SELECT machine_id, username, time_started, 0 AS available 
                                FROM Machine NATURAL JOIN UsingMachine
                            ) inUseMachines
                            WHERE NOT machine_id=''
                    ''' )
    all_machine_tuples = cursor.fetchall()

    for t in all_machine_tuples:
        machines.append({  'machine-id' : t[0], 'machine-type' : t[1], 'location' : t[2],    
                            'username' : t[3], 'time-remaining' : helper.getTimeRemaining(int(t[4])), 'available' : bool(t[5]) })

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
    if(len(cursor.fetchall()) != 0): 
        # close the database connection
        cursor.close()
        return True
    else:
        # close the database connection
        cursor.close()
        return False


# Global variable to store form information until users can be added to the database
# FIXME is this a security issue?
verificationDict = {}

#Stores form data with the verification code as the key
def storeUser(form, verificationCode):
    verificationDict[verificationCode] = form

# Registers a new user in the database (from verification code)
# Returns new user's username (for use in other functions)
def verifyUser(verificationCode):
    username = registerUser(verificationDict[verificationCode])
    verificationDict.pop(verificationCode)
    return username

# Registers a new user in the database (from form data)
# Returns new user's username (for use in other functions)
def registerUser(form):
    # connect to the database with cursor
    # TODO use ACID transactions to help with concurrent queries
    #   - set transaction isolation level serializable
    cursor = mysql.connection.cursor()

    # First, salt and hash the password and store all of the info in the database
    # the password is only now pulled from the form
    pass_hash = helper.generateHashAndSalt(str(form['password']))

    cursor.execute( ('''INSERT INTO MachineUser VALUES (%s, %s, %s, %s, %s)'''), 
                    (str(form['email']), str(form['username']), str(form['preferredRoom']), str(pass_hash[0]), str(pass_hash[1])) )

    # close the database connection
    cursor.close()
    mysql.connection.commit()
    return form['username']


# Updates a current user in the database
# Returns 0 if successful, otherwise 1
def updateUser(oldEmail, newEmail, username, password):
    #TODO update user data based on oldEmail (email may or may not change)
    return 0


# Returns the data for a user based on username
def getUserData(username):
    #TODO get user data based on username
    return {'email':'user@gmail.com','username':'testUser','preferredRoom':'222W Wads (Armada/Citadel)'}

# Checks if a user is an admin, returns 1 if admin, otherwise 0
def isAdmin(username):
    #TODO get user admin status based on username
    #TEMP two different users with different status
    if(username == 'ekrummer'):
        return 1
    else:
        return 0


# Returns the preferred room for a user based on username
def getPreferredRoom(username):
    #TODO get room based on username
    return "356E Wads (Danger Zone/Valhalla)";


# Returns a list of machines that the user has checked out
def getUserMachines(username):
    machines = []                           # array holds all machines

    cursor = mysql.connection.cursor()      # open database connection

    # all machines, doesn't show whether or not they are in use.
    cursor.execute( ''' 
                        SELECT machine_id, machine_type, location, time_started
                        FROM UsingMachine NATURAL JOIN Machine
                        WHERE username = %s
                    ''', (username,) )
    all_machine_tuples = cursor.fetchall()

    for t in all_machine_tuples:
        machines.append({  'machine-id' : t[0], 'machine-type' : t[1], 'location' : t[2], 
                            'time-remaining' : helper.getTimeRemaining(int(t[3]))  })

    cursor.close()

    # return the list as an array
    return machines



# Marks a machine as checked out to a user
def checkout(machineID, username):
    #TODO checkout(machineID, username)
    # update UsingMachine with the correct info
    # TODO get the user email

    cursor = mysql.connection.cursor()
    # get the user's email
    cursor.execute(''' SELECT email FROM MachineUser WHERE username=%s ''', (username,))
    t = cursor.fetchall()
    email = t[0]

    # add this machine to the UsingMachine table
    # TODO isolated transactions with a write lock so that simultaneous writes cannot occur
    cursor.execute(''' INSERT INTO UsingMachine VALUE (%s, %s, %s, %s) ''', (machineID, email, username, helper.getCurrentTime()))

    cursor.close()
    mysql.connection.commit()

    print(machineID + " checked out to " + username)
    return 0



# Marks a machine as checked in by a user
def checkin(machineID, username):
    cursor = mysql.connection.cursor()

    #TODO WRITE LOCK
    # remove this machine from the UsingMachine table
    cursor.execute(''' DELETE FROM UsingMachine WHERE machine_id=%s AND username=%s ''', (machineID, username))

    cursor.close()
    mysql.connection.commit()

    print(machineID + " checked in by " + username)
    return 0
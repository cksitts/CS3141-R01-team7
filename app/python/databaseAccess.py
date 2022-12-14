from flask import current_app
from app.python import helper

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    # get this user's data if it exists
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s OR email=%s ''', (username, username))

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
    rooms = []                   # array holds room strings

    cursor = current_app.config['MYSQL'].cursor()      # open database connection
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

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

    cursor.execute(''' COMMIT ''')
    cursor.close()

    # return the list as an array
    return rooms


# Returns a list of locations (hall names) from the database
def getLocations():
    halls = []                           # array holds hall strings

    cursor = current_app.config['MYSQL'].cursor()      # open database connection

    # all distinct locations
    cursor.execute( ''' SELECT DISTINCT location FROM Machine WHERE NOT location='' ''' )
    all_hall_tuples = cursor.fetchall()

    for t in all_hall_tuples:
        halls.append(t[0])

    cursor.close()

    # return the list as an array
    return halls


# Returns a list of all machines and their data from the database
#   - maintains information about which machines are in use and by whom
def getAllMachines():
    machines = []                           # array holds all machines

    cursor = current_app.config['MYSQL'].cursor()      # open database connection

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

# Checks if login is potentially valid
# return a status code
# - 0 if success
# - 1 if email is taken
# - 2 if username is taken
# - 3 if both are taken
def checkEmailAndUsernameTaken(email, username):
     # connect to the database with cursor
    #   - set transaction isolation level serializable
    cursor = current_app.config['MYSQL'].cursor()

    # check the database to see if the email already exists
    cursor.execute( '''SELECT * FROM MachineUser WHERE email=%s''', (email,) )
    email_code = 0
    if(len(cursor.fetchall()) != 0): 
        email_code = 1
    
    # check the database to see if the username already exists
    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (username,))
    username_code = 0
    if (len(cursor.fetchall()) != 0):
        username_code = 2

    return email_code + username_code

# Registers a new user in the database (from form data)
# Returns new user's username (for use in other functions)
def registerUser(storedUser):
    # connect to the database with cursor
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE')
    cursor.execute('START TRANSACTION')

    # First, salt and hash the password and store all of the info in the database
    # the password is only now pulled from the form
    pass_hash = helper.generateHashAndSalt(str(storedUser['password']))

    cursor.execute( ('''INSERT INTO MachineUser VALUES (%s, %s, %s, %s, %s)'''), 
                    (   str(storedUser['email']), 
                        str(storedUser['username']), 
                        str(storedUser['preferredRoom']), 
                        str(pass_hash[0]), 
                        str(pass_hash[1])) )

    # if there was an error in inserting or if the transaction timed out
    cursor.execute(''' SELECT * FROM MachineUser WHERE email=%s ''', (storedUser['email'],))
    if (len(cursor.fetchall()) == 0):
        cursor.execute('ROLLBACK')
        cursor.close()
        current_app.config['MYSQL'].commit()
        return None

    # no errors: close the database connection and return the username
    cursor.execute('COMMIT')
    cursor.close()
    current_app.config['MYSQL'].commit()

    return storedUser['username']

# change the password info at "username" using the new "password"
def changePassword(username, password):
    cursor = current_app.config['MYSQL'].cursor()
    pass_info = helper.generateHashAndSalt(password)
    cursor.execute(''' UPDATE MachineUser SET pass_hash=%s, pass_salt=%s WHERE username=%s ''', (pass_info[0], pass_info[1], username))

# Updates a current user in the database
# Returns a status code:
#   0: success
#   1: email error (used for displaying)
#   2: username error (used for displaying)
#   3: both email and username error (used for displaying)
#   -1: incorrect password
def updateUser(oldEmail, newEmail, oldUsername, newUsername, password):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

    status_code = 0

    # if username changed
    if (oldUsername != newUsername):
        # is the new username taken?
        cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (newUsername,))
        if (len(cursor.fetchall()) != 0):
            status_code += 2

    # if email changed
    if (oldEmail != newEmail):
        # is the new email taken?
        cursor.execute(''' SELECT * FROM MachineUser WHERE email=%s ''', (newEmail,))
        if (len(cursor.fetchall()) != 0):
            status_code += 1

    if (status_code != 0):
        return status_code
        
    # update the database with the new information if the password entered is correct
    # get the salt for the password
    cursor.execute(''' SELECT pass_hash, pass_salt FROM MachineUser WHERE email=%s ''', (oldEmail,))
    t = cursor.fetchall()[0]
    hash = t[0]
    salt = t[1]

    if (helper.getHash( password + salt ) == hash):
        cursor.execute('''  UPDATE MachineUser SET email=%s, username=%s
                            WHERE email=%s''', (newEmail, newUsername, oldEmail))

        cursor.execute(''' COMMIT ''')
        cursor.close()
    else:
        status_code = -1
    
    return status_code

# delete a user's account data from the database
#   - UsingMachine data is also deleted
def deleteUser(email):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED ''')
    cursor.execute(''' START TRANSACTION ''')

    cursor.execute(''' DELETE FROM MachineUser WHERE email=%s ''', (email,))
    cursor.execute(''' SELECT * FROM MachineUser WHERE email=%s ''', (email,))
    if (len(cursor.fetchall()) != 0):
        cursor.execute(''' ROLLBACK ''')
        return False

    cursor.execute(''' COMMIT ''')
    cursor.close()
    current_app.config['MYSQL'].commit()
    return True


# Get a user's username given their email (used to initialize session)
def getUsernameFromEmail(email):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SELECT username FROM MachineUser WHERE email=%s ''', (email,) )

    username = cursor.fetchall()[0]
    
    cursor.close()
    current_app.config['MYSQL'].commit()

    return username[0]

# Returns the data for a user based on username
# if there is no user data, return None
def getUserData(username):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

    # get the user from the database
    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (username,))
    r = cursor.fetchall()

    # if something goes wrong in the query, return an error and rollback
    if (len(r) == 0):
        print("Error: could not get user data.")
        cursor.execute(''' ROLLBACK ''')
        return None

    t = r[0]
    cursor.execute(''' COMMIT ''')
    cursor.close()
    return {'email' : t[0], 'username' : t[1], 'preferredRoom' :  t[2]}

# Checks if a user is an admin, returns 1 if admin, otherwise 0
def isAdmin(username):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    
    #get user's email and check if they are an admin
    email = getUserData(username)['email']
    cursor.execute(''' SELECT * FROM MachineUser NATURAL JOIN Administrator WHERE email=%s''', (email,))

    result = cursor.fetchall()
    if (len(result) != 0):
        return True
    else:
        return False


# Returns a list of machines that the user has checked out
def getUserMachines(username):
    machines = []                           # array holds all machines

    cursor = current_app.config['MYSQL'].cursor()

    # all machines, doesn't show whether or not they are in use.
    cursor.execute( ''' SELECT machine_id, machine_type, location, time_started
                            FROM UsingMachine NATURAL JOIN Machine
                            WHERE username = %s ''', (username,) )

    all_machine_tuples = cursor.fetchall()

    for t in all_machine_tuples:
        machines.append({  'machine-id' : t[0], 'machine-type' : t[1], 'location' : t[2], 
                            'time-remaining' : helper.getTimeRemaining(int(t[3]))  })

    cursor.close()
    current_app.config['MYSQL'].commit()

    # return the list as an array
    return machines


# Adds a machine to the database
# Returns a status code:
#   - 0 if successful
#   - 1 if machine is already in the database
#   - 2 if the database failed to add the machine
def addMachine(machineID, location, type):
    cursor = current_app.config['MYSQL'].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')

    # check if the machine id is already in the database
    cursor.execute('''SELECT * FROM Machine WHERE machine_id=%s''', (machineID,))
    all_machine_tuples = cursor.fetchall()
    
    if(len(all_machine_tuples) != 0):
        cursor.execute(''' ROLLBACK ''')
        return 1 #fail - machine already in database


    # store the new machine in the database
    cursor.execute( '''INSERT INTO Machine VALUES (%s, %s, %s)''', (machineID, location, type) )

    # ensure machine storage went well
    cursor.execute(''' SELECT * FROM Machine WHERE machine_id=%s ''', (machineID,))
    if (len(cursor.fetchall()) == 0):
        cursor.execute(''' ROLLBACK ''')
        return 2

    # close the database connection
    cursor.execute(''' COMMIT ''')
    cursor.close()
    current_app.config['MYSQL'].commit()

    return 0 #success


# Marks a machine as checked out to a user
def checkout(machineID, username):
    # update UsingMachine with the correct info

    cursor = current_app.config['MYSQL'].cursor()
    # get the user's email
    cursor.execute(''' SELECT email FROM MachineUser WHERE username=%s ''', (username,))
    t = cursor.fetchall()
    if (len(t) == 0):
        return 1
    email = (t[0])[0]

    print((machineID, email, username, helper.getCurrentTime()))

    # add this machine to the UsingMachine table
    cursor.execute(''' INSERT INTO UsingMachine VALUE (%s, %s, %s, %s) ''', (machineID, email, username, helper.getCurrentTime()))

    cursor.close()
    current_app.config['MYSQL'].commit()

    print(machineID + " checked out to " + username)
    return 0



# Marks a machine as checked in by a user
def checkin(machineID, username):
    cursor = current_app.config['MYSQL'].cursor()

    # remove this machine from the UsingMachine table
    cursor.execute(''' DELETE FROM UsingMachine WHERE machine_id=%s AND username=%s ''', (machineID, username))

    cursor.close()
    current_app.config['MYSQL'].commit()

    print(machineID + " checked in by " + username)
    return 0
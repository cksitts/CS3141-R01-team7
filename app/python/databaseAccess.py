from app import mysql
from app.python import helper
from time import time

# Checks if a given username/password is in the database
# Returns true if valid, otherwise false
def validLogin(username, password):
    cursor = mysql.connection.cursor()

    # get this user's data if it exists
    cursor.execute(''' SELECT * FROM MachineUser WHERE username=%s ''', (str(username),))
    tuple = cursor.fetchone()
    if tuple != None:
        # username is in the database so get the password hash
        t_hash = tuple[2]                                           # get the password hash stored in the
        hash = helper.getHash( str(password + tuple[3]) )           # generate a hash to compare
        return hash == t_hash                                       # return true if the generated hash equals the stored hash

    return False


# Returns a list of laundry rooms from the database
def getLaundryRooms():
    rooms = []                           # array holds room strings

    cursor = mysql.connection.cursor()      # open database connection

    # all distinct room numbers and their building
    cursor.execute( '''     SELECT DISTINCT
	                            SUBSTRING_INDEX(machine_id, '_', 1) as Room,
                                SUBSTRING_INDEX(substring_index(machine_id, '_', -2), '_' ,1) as Building
                            FROM Machine;
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
    cursor.execute( '''     SELECT DISTINCT
	                        LOCATION as Location
                            from Machine;
                    ''' )
    all_room_tuples = cursor.fetchall()

    i = 0
    for t in all_room_tuples:
        rooms[i] = rooms[i] + " (" + t[0] + ")"
        i += 1

    cursor.close()

    # return the list as an array
    print(rooms)
    return rooms


# Returns a list of all machines and their data from the database
# TODO machines that are specifically in use (we will just have to decide how we want to get this data)
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
                    ''' )
    all_machine_tuples = cursor.fetchall()

    for t in all_machine_tuples:
        start_time = int(t[4])                                  # start time (SEC) 1666901715
        current_time = int(time())
        time_elapsed = int( (current_time - start_time) / 60 )      # the time that the machine has left until finishing (MIN)
        time_remaining = (60 - time_elapsed) if (time_elapsed < 60 and time_elapsed >= 0) else 0

        machines.append({  'machine-id' : t[0], 'machine-type' : t[1], 'location' : t[2],    
                            'username' : t[3], 'time-remaining' : time_remaining, 'available' : bool(t[5]) })

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


# Updates a current user in the database
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
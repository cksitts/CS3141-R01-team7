import secrets
from hashlib import sha256
from time import time

"""
Generate just a hash for an input string.
@param str: the string to hash
@return a string of the hash's hexadecimal digest
"""
def getHash(string: str):
    return str( sha256(string.encode()).hexdigest() )

"""
Generate a password's salt, then hash it
@param password: the password to hash
@return a tuple with the hash and the salt added before hashing
"""
def generateHashAndSalt(password):
    # generate a salt string
    length = secrets.randbelow(11) + 5                           # random length in [5,15]
    char_offset = 0
    printable_char_code = 65;                                    # character from ascii 65 = A
    
    salt = ""
    
    for c in range(0, length + 1):
        char_offset = secrets.randbelow(90);                     # choose a random character 
        new_char = chr(printable_char_code + char_offset);       # store that character
        salt += new_char;                                        # add that character to the salt sequence

    # hash the password with the salt string
    _hash = getHash( str(password + salt) )

    return [_hash, salt]                             # return the tuple

#Returns the time remaining given a machine start time
def getTimeRemaining(startTime): # start time (SEC)
    current_time = int(time())
    time_elapsed = int( (current_time - startTime) / 60 )      # the time that the machine has left until finishing (MIN)
    return (60 - time_elapsed) if (time_elapsed < 60 and time_elapsed >= 0) else 0

# Returns the current time as an integer in the form that other functions expect
def getCurrentTime():
    return int(time())

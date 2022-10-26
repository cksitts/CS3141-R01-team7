import secrets
from hashlib import sha256

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
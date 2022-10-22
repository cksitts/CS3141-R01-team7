# File holds the methods that help with the signup process
from app.python.send_email import sendEmail
import secrets
from hashlib import sha256

"""
Function to send an email with a verification code specifically for signups
@param to: the address to send the message to
@return the code that was sent so that it can be verified
"""
def sendSignupEmail(to):
    # generate a random verification code using a random hex sequence
    # the length of the sequence is 6 total digits (3 bytes converted to 2 digits each)
    code_length = 3
    code = str(secrets.token_hex(code_length)).upper()
    sendEmail("Enter Verification Code: %s" % code, to)
    return code

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
    _hash = sha256( str(password + salt).encode() )

    return [_hash.hexdigest(), salt]                             # return the tuple
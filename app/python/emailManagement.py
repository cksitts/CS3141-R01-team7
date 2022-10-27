import secrets
import smtplib
import os
from waiting import wait, TimeoutExpired

from app.python import constant


# function drafts and sends an email with Subject: "Laundry Tracker Lite"
# the message body and the receiver is provided as a string to this function
def sendEmail(message, to):
    e_password = os.environ.get("TSP_EMAIL_PASS")   # get email and password for sender
    e_user = os.environ.get('TSP_EMAIL')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()         # open an smtp connection (called by default)
        smtp.starttls()     # change connection type to encrypted (standard TLS encryption)
        smtp.ehlo()         # restart the connection with TLS

        smtp.login(e_user, e_password)  # login to email account via smtp server

        subject = 'Laundry Tracker Lite!'
        body = message

        msg = 'Subject:%s\n\n%s' % (subject, body)

        smtp.sendmail(e_user, to, msg) # send a message (from, to, msg)



"""
Function to send an email with a verification link specifically for signups
@param to: the address to send the message to
@param url: the root url of the website
@return the verification code
"""
def sendSignupEmail(to, url):
    # generate a random verification code using a random hex sequence
    # the length of the sequence is 6 total digits (3 bytes converted to 2 digits each)
    code_length = 3
    code = str(secrets.token_hex(code_length)).upper()
    sendEmail("Your link will expire in 5 minutes.\nClick to verify: {}verify/{}".format(url,code), to)
    print("Click to verify: {}verify/{}".format(url,code)) #TEMP prints the verification link as well as emailing
    return code


#Global variable to keep track of which codes still need to be verified
verificationDict = {}

# Validates an email
# Returns true if valid, otherwise false
def isValid(email, url) :
    code = sendSignupEmail(email, url) #sends an email with a verification link
    verificationDict[code] = False #adds the code to the verificationDict
    try:
        # waits until the user goes to the verification page
        wait(lambda : True if verificationDict[code] == True else False, timeout_seconds = constant.VERIFICATION_TIMEOUT)
    except TimeoutExpired:
        # timed out
        return False
    verificationDict.pop(code) #removes the code from the verificationDict
    return True

# Sets a verification code in the dict as verified
def verifyCode(code):
    if(code in verificationDict):
        verificationDict[code] = True
        return 0
    else:
        return 1
import secrets
import smtplib
import os
import smtplib
from email.message import EmailMessage

# function drafts and sends an email with Subject: "Laundry Tracker Lite"
# the message body and the receiver is provided as a string to this function
def sendEmail(message, to):
	e_password = os.environ.get("EMAIL_PASS")   # get email and password for sender
	e_user = os.environ.get('EMAIL')
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()         # open an smtp connection (called by default)
		smtp.starttls()     # change connection type to encrypted (standard TLS encryption)
		smtp.ehlo()         # restart the connection with TLS

		smtp.login(e_user, e_password)  # login to email account via smtp server

		msg = EmailMessage()
		msg['Subject'] = 'Laundry Tracker Lite Sign up Code'
		msg['From'] = 'Laundry Tracker Lite'
		msg['To'] =  to

		msg.set_content(message, subtype='html')

        # subject = 'Laundry Tracker Lite!'
        # body = message

        # msg = 'Subject:%s\n\n%s' % (subject, body)

        #smtp.sendmail(msg) # send a message (from, to, msg)

		smtp.send_message(msg)



"""
Function to send an email with a verification code specifically for signups
@param to: the address to send the message to
@param url: the root url of the website
@return the verification code
"""
def sendSignupEmail(to):
    # generate a random verification code using a random hex sequence
    # the length of the sequence is 6 total digits (3 bytes converted to 2 digits each)
    code_length = 3
    code = str(secrets.token_hex(code_length)).upper()

    relative_path = "../static/emailTemplates/verificationEmail.html"
    email_html = open(os.path.join(os.path.split(os.path.abspath(__file__))[0], relative_path), mode='rt').read().replace("{CODE}", code)

    sendEmail(email_html, to)
    print("Verification code: %s" % code) #TEMP prints the verification link as well as emailing
    return code

"""
Function to send an email with a verification code specifically for password resets
@param to: the address to send the message to
@param url: the root url of the website
@return the verification code
"""
def sendPasswordResetEmail(to):
    # generate a random verification code using a random hex sequence
    # the length of the sequence is 6 total digits (3 bytes converted to 2 digits each)
    code_length = 3
    code = str(secrets.token_hex(code_length)).upper()

    relative_path = "../static/emailTemplates/passwordResetEmail.html"
    email_html = open(os.path.join(os.path.split(os.path.abspath(__file__))[0], relative_path), mode='rt').read().replace("{CODE}", code)

    sendEmail(email_html, to)
    print("Verification code: %s" % code) #TEMP prints the verification link as well as emailing
    return code
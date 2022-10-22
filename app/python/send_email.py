# Helper script to send an email to a user
# Author: Tristan Sorenson

import smtplib
import os

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

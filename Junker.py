from flask import Flask, render_template, request
import smtplib
import time
import imaplib
import email
import re
import random
import easyimap
from string import Template
import quopri
import sys
import os

sys.path.append('/var/www/Junker')
path = os.path.abspath('/var/www/Junker/templates')
application = Flask(__name__, template_folder=path)


@application.route('/')
def hello_world():
    ids = random.randint(0, 10000)


    if "pastemail" in request.cookies:
        p = re.compile('\d+')
        found = p.search(request.cookies['pastemail'])

        if found:
            idmatch = found.group()
            ids = idmatch

    #matches = get_email_from_gmail(str(ids))
    matches = read_email_from_gmail(str(4600))
  # matches = ""
    emails = "junkeremailservices+" + str(ids) + "@gmail.com"

    #print(matches)
  # print(type(retval))

    return render_template('index.html', email=emails, emailmatch=matches)


def get_email_from_gmail(idhere):

    host = "imap.gmail.com"


    user = "junkeremailservices@gmail.com"
    password = "junkeremail"
    mailbox = "INBOX"
    imapper = easyimap.connect(host, user, password, mailbox)
    mails = imapper.listup(limit=50)
    p = re.compile('\d+')
    emails = []

    for item in mails:
        found = p.search(item.to)

    if found:
        idofemail = found.group()
        # print("ID of Email: ")
        # print(idofemail)
        # print("ID: ")
        # print(idhere)


        if idofemail == str(idhere):
        #print("In emails with ID: " + idofemail + " and master id : " + str(idhere))
            emails.append("<h6>From : " + item.from_addr + "</h6><h7>" + "To : " + item.to + "</h7><br><p>" + item.body + "</p>")
    endstr = ""

    for temp in emails:
        endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"

    return endstr







def read_email_from_gmail(id):
      # try:


    from_email = "junkeremailservices@gmail.com"
    from_pwd = "junkeremail"
    mail = imaplib.IMAP4_SSL("smtp.gmail.com")
    mail.login(from_email, from_pwd)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    f = open("emailout.txt", "w+")
    emails = []


    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                #print(msg.keys())
                email_from = str(msg['from'])
                email_to = msg['to']
                email_body = ""
                for part in msg.walk():
                    email_body = part.get_payload(None, True)
                    #print ">****<"
                    #print temp
                    #print "<****>"
                # if msg.is_multipart():
                #     for payload in msg.get_payload():
                #         #email_body = email_body + payload + "\n"
                #         print ""
                #         print "****"
                #         print payload.keys()
                #         print payload['Content-Type']
                #         print "****"
                #         print payload['Content-Transfer-Encoding']
                #         if payload['Content-Transfer-Encoding'] == 'quoted-printable' or payload['Content-Transfer-Encoding'] == None:
                #             print quopri.decodestring(payload)
                #         print "****"
                #         print ""

                    p = re.compile('\d+')
                    search = p.search(email_to)
                    if search:
                        email_id = search.group()
                        print("Inside Search Bool")
                        print("Email ID = " + str(email_id))

                        print("Regular ID = " + str(id))

                        if email_id == id:
                            print("Equals each other" + str(id) + " == " + str(email_id))
                            if email_body is not None:
                                emails.append("<h6>From : " + email_from + "</h6>" + "<h7>To : " + email_to + "</h7>" + "<p>" + email_body + "</p>")
    endstr = ""
    for temp in emails:
                endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"
    print endstr
    return (endstr)

if __name__ == '__main__':
#    application.debug = True
    application.run('0.0.0.0', 5000)

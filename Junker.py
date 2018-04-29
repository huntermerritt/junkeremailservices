
from flask import Flask, render_template, request
import smtplib
import time
import imaplib
import email
import re
import random
import JunkerTempHolder
import easyimap
from string import Template

application = Flask(__name__)


@application.route('/')
def hello_world():
    ids = random.randint(0,10000)

    if "pastemail" in request.cookies:
        p = re.compile('\d+')
        found = p.search(request.cookies['pastemail'])
        if found:
            idmatch = found.group()
            ids = idmatch

    matches = get_email_from_gmail(str(4376))
    #matches = ""
    emails = "junkeremailservices+" + str(ids) + "@gmail.com"
    #print(matches)
    retval = JunkerTempHolder.getTheJunker()
    print(type(retval))
    return retval.substitute(email="", emailmatch="")


def get_email_from_gmail(idhere):
    host = "imap.gmail.com"
    user = "junkeremailservices@gmail.com"
    password = "junkeremail"
    mailbox = "INBOX"
    temps = open("errorsfound.txt", "w+")
    temps.write("Before easyimap.connect\n")
    imapper = easyimap.connect(host, user, password, mailbox)
    #temps.write("After easyimap.connect\n")
    mails = imapper.listup(limit=50)
    #temps.write("After imapper.listup\n")
    p = re.compile('\d+')
    emails = []
    for item in mails:
	temps.write("Goint through the mails now\n")
        found = p.search(item.to)
        if found:
	    temps.write("Found a good one\n")
            idofemail = found.group()
            print("ID of Email: ")
            print(idofemail)
            print("ID: ")
            print(idhere)

            if idofemail == str(idhere):
		temps.write("Found where the id matches each other\n")
                print("In emails with ID: " + idofemail + " and master id : " + str(idhere))
                emails.append("<h6>From : " + item.from_addr + "</h6><h7>" + "To : " + item.to + "</h7><br><p>" + item.body + "</p>")
    endstr = ""
    for temp in emails:
	temps.write("Building end string\n")
        endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"
    temps.write(endstr)
    endstr = ""
    return endstr




def read_email_from_gmail(id):
    #try:
        from_email = "junkeremailservices@gmail.com"
        from_pwd = "junkeremail"
        mail = imaplib.IMAP4_SSL("smtp.gmail.com")
        mail.login(from_email,from_pwd)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        f = open("emailout.txt", "w+")
        emails = []

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    print(msg.keys())
                    email_from = str(msg['from'])
                    email_to = msg['to']
                    email_body = ""
                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            email_body = email_body + payload + "\n"
                    p = re.compile('\d+')
                    search = p.search(email_to)

                    if search:
                        email_id = search.group()
                        print("Inside Search Bool")
                        print("Email ID = " + str(email_id))
                        print("Regular ID = " + str(id))
                        if email_id == id:
                            print("Equals each other" + str(id) + " == " + str(email_id))
                            f.write('From : ' + email_from + '\n')
                            f.write('Subject : ' + email_subject + '\n')
                            f.write('T0 : ' + email_to + '\n')
                            emails.append("<h6>From : " + email_from + "</h6>" + "<h7>To : " + email_to + "</h7>" + "<p>" + email_body + "</p>")
        endstr = ""
        for temp in emails:
            endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"
        return (endstr)
    #except Exception:
    #    print(str(Exception) + " WRONG")


if __name__ == '__main__':
    application.run(host='0.0.0.0')

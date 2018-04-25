from flask import Flask, render_template
import smtplib
import time
import imaplib
import email
import re
import random

application = Flask(__name__)


@application.route('/')
def hello_world():
    id = random.randint(0,10000)
    matches = read_email_from_gmail(str(id))
    email = "junkeremailservices" + str(id) + "@gmail.com"
    print(matches)

    return render_template('index.html', emailmatch=read_email_from_gmail(str(id)), email="junkeremailservices+" + id + "@gmail.com")


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
                        if email_id == id:
                            f.write('From : ' + email_from + '\n')
                            f.write('Subject : ' + email_subject + '\n')
                            f.write('T0 : ' + email_to + '\n')
                            emails.append("From : " + email_from + "\n" + "TO : " + email_to + "\n" + email_body)
        endstr = ""
        for temp in emails:
            endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"
        return (endstr)
    #except Exception:
    #    print(str(Exception) + " WRONG")


if __name__ == '__main__':
    read_email_from_gmail("1245")
    application.run(host='0.0.0.0')

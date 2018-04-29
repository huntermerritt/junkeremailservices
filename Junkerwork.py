from flask import Flask, request
import imaplib
import email
import re
import random
import JunkerTempHolder
import easyimap
from string import Template

application = Flask(__name__)

thisstr = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Junker Email Services</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">


</head>
<style>

    body
    {
        background: url('../static/a24d7c65b659b52eeb1016a0c35b7ad3 copy.jpg');
        background-size: cover;
    }
    .message
    {
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.31);
        border-radius: 10px;
        color: black;
        height: 25vh;
        overflow-y: scroll;
    }
</style>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-dark">
    <a class="navbar-brand" href="#"><h3 style="color: orange; font-family: 'Snell Roundhand'">Junker Email Services</h3></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
        </div>
    </div>
</nav>

<div class="container">
    <div class="row">
        <div class="col-3" style="height: 100vh; background-color: transparent">

        </div>

        <div class="col-7" style="background-color: transparent; overflow-y: scroll;">
            <br>
            <div class="message">
                <p>Your Current Temporary Email Address is: {email}</p>
            </div>
            {emailmatch}

        </div>

        <div class="col-2" style="background-color: transparent;">

        </div>

    </div>

</div>


</body>
</html>
'''

@application.route('/')
def hello_world():
    ids = random.randint(0,10000)

    if "pastemail" in request.cookies:
        p = re.compile('\d+')
        found = p.search(request.cookies['pastemail'])
        if found:
            idmatch = found.group()
            ids = idmatch

    matches = get_email_from_gmail(str(ids))
    emails = "junkeremailservices+" + str(ids) + "@gmail.com"
    print(matches)
    retval = JunkerTempHolder.getTheJunker()
    print(type(retval))
    thisstr.replace('{email}', emails)
    thisstr.replace('{emailholder}', matches)
    return thisstr


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
            print("ID of Email: ")
            print(idofemail)
            print("ID: ")
            print(idhere)

            if idofemail == str(idhere):
                print("In emails with ID: " + idofemail + " and master id : " + str(idhere))
                emails.append("<h6>From : " + item.from_addr + "</h6><h7>" + "To : " + item.to + "</h7><br><p>" + item.body + "</p>")
    endstr = ""
    for temp in emails:
        endstr = endstr + "<br>" + "<div class=message>" + temp + "</div>" + "<br>"
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

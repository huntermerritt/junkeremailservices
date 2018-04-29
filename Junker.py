from flask import Flask, render_template, request
import easyimap
import random
import re

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
    ids = random.randint(0, 10000)
    ids = str(ids)
    #if "pastemail" in request.cookies:
    #    p = re.compile('\d+')
    #    found = p.search(request.cookies['pastemail'])
    #    if found:
    #        idmatch = found.group()
    #        ids = idmatch

    matches = get_email_from_gmail(ids)
    emails = "junkeremailservices+" + str(ids) + "@gmail.com"
    thisstr.replace('{email}', emails)
    thisstr.replace('{emailholder}', matches)
    return thisstr

def get_email_from_gmail(ids):
    a = ids

def get_email_from_gmails(idhere):
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



if __name__ == '__main__':
    application.run(host='0.0.0.0')

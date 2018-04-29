from flask import Flask, render_template
import poplib, email

application = Flask(__name__)


@application.route('/')
def hello_world():

    mailserver = 'pop.gmail.com'
    emailid = 'junkeremailservices@gmail.com'
    emailpass = 'junkeremail'

    myconnection = poplib.POP3_SSL(mailserver)

    myconnection.user(emailid)
    myconnection.pass_(emailpass)

    emailinfo = myconnection.stat()

    numbermail = emailinfo[0]

    for i in range(numbermail):
        for emails in myconnection.retr(i + 1)[1]:
            print emails

    return render_template('index.html', email='junker', emailmatch='emailmatch')



if __name__ == '__main__':
    application.run(host='0.0.0.0')

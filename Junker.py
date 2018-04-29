from flask import Flask, render_template
import smtplib, email, time, imaplib

application = Flask(__name__)


@application.route('/')
def hello_world():

    mailserver = 'imap.gmail.com'
    emailid = 'junkeremailservices@gmail.com'
    emailpass = 'junkeremail'
    smtp_port = 993
    end_str = ""
    try:
	end_str += "This is the beginning"
        mail = imaplib.IMAP4_SSL(mailserver, 465)
	end_str += "This is after ssl"
        mail.login(emailid, emailpass)
	end_str += "This is after login"
        mail.select('inbox')
	end_str += "This is after the mail logins"
        type, data = mail.search(None, 'ALL')
	end_str += "Set the type and data"
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
	end_str += "Added the first and last email"

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
	    end_str += "In the first for loop"

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
		    end_str = 'From : '
		    

    except Exception, e:
        end_str += str(e)
	print str(e)

    return render_template('index.html', email='junker', emailmatch=str(end_str))



if __name__ == '__main__':
    application.run(host='0.0.0.0')

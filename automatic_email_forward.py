import imaplib
import email
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from languages.ge import ge
from languages.en import en
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

#get language infos
selected_language = config['General']['language']
languages = {"german": ge, "english": en}
dateTimeObj = datetime.now()
time = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")

def main():
    logging.basicConfig(filename="logfile.log", level=logging.INFO)

    #endless loop, always checking for new emails
    while 1:
        getMail(config)

def getMail(config):
    #log into server
    try:
        server = imaplib.IMAP4_SSL(config['RECEIVE EMAIL']['host'], config['RECEIVE EMAIL']['port'])
    except OSError as e:
        logging.error(time + ': ' + str(e))
        return

    try:
        server.login(config['RECEIVE EMAIL']['name'], config['RECEIVE EMAIL']['password'])
    except server.error as e:
        if 'Invalid credentials' in str(e):
            print(languages[selected_language]["password incorrect"])
            return
        if 'LOGIN Server error' in str(e):
            logging.error(time +': LOGIN Server error')
            return
        else:
            logging.error(time + ': ' + str(e))
            return

    #select mailbox
    mailbox = config['RECEIVE EMAIL']['mailbox']
    server.select(mailbox)

    #loop through all unread emails
    typ, data = server.search(None, 'UNSEEN')
    try:
        for num in data[0].split():
            typ, data = server.fetch(num, '(RFC822)')
            email_data = data[0][1]
            modifyMail(email_data, config)
    except server.error as e:
        logging.error(time + ': ' + str(e))
        return
    except OSError as e:
        logging.error(time + ': ' + str(e))
        return
    server.close()
    server.logout()

def modifyMail(data, config):
    # create a Message instance from the email data
    message = email.message_from_bytes(data)
    sender = message.get('From', 'utf-8')
    subject = message.get('Subject')

    #add the original sender to the subject
    message.replace_header("Subject", subject + "  (" + languages[selected_language]["original sender"] +" " + sender + ")")
    message.replace_header("To", config['SEND EMAIL']['targets'])
    message.replace_header("From", config['SEND EMAIL']['sender'])

    sentMail(message, config, sender, subject)

def sentMail(message, config, sender, subject):
    #log into smtp
    smtp = smtplib.SMTP_SSL(config['SEND EMAIL']['host'], config['SEND EMAIL']['port'])
    smtp.login(config['SEND EMAIL']['name'], config['SEND EMAIL']['password'])
    try:
        smtp.sendmail('prispapierabwi@aol.com', 'abraham@prismapapier.de', message.as_string())
        logging.info(time +': ' + languages[selected_language]["email forwardet"])
    except:
        #If the email is blocked by the receiver, a email is send, that something was blocked
        spam_mail = MIMEMultipart("alternative")
        spam_mail["Subject"] = languages[selected_language]["spam_subject"]
        spam_mail["From"] = "prispapierabwi@aol.com"
        spam_mail["To"] = "abraham@prismapapier.de"
        spam_text = languages[selected_language]["sender"] + " " + sender + " " + languages[selected_language]["subject"] + " " + subject + " " + languages[selected_language]["block"]

        part1 = MIMEText(spam_text, 'plain', 'utf-8')
        spam_mail.attach(part1)

        smtp.sendmail('prispapierabwi@aol.com', 'abraham@prismapapier.de', spam_mail.as_string())
        logging.info(time +': ' + languages[selected_language]["spam forwardet"])
    smtp.quit()


if __name__ == "__main__":
    main()

import imaplib
import smtplib
import email
import email.header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import apiai
import json
import sys
import time


def check_message(login, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.list()
    mail.select("inbox")

    resultes, data = mail.search(None, "ALL")
    index_list = data[0].split()
    results = index_list[-1].decode("utf-8")
    results = int(results)

    last_message_id = open("lastid.txt", "w")
    last_message_id.write(str(results))
    last_message_id.close()


def message(login, password, from_user):
    msg = MIMEMultipart()

    msg["From"] = login
    msg["Subject"] = "Это тебя заинтересует)"

    body = '''
    Привет)) Это тебя заинтересует)\n

    Знакомства для секса, для общения и для создания семьи, совершенно бесплатно)\n
    Вот тебе 2 сайта, обе бесплатные, там куча женщин и девушек для секса и для общения\n
    Сайт №1 👉  https://bit.ly/3cmsBK4\n
    Сайт №2 👉  https://is.gd/AGoBj3\n

    Зарегистрируйся в обоих сайтах! Там все бесплатно! Платить ничего не надо!!! Секс гарантирован!\n
    Я сижу только там, тут не отвечаю.'''

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(login, password)
    server.sendmail(login, from_user, msg.as_string())
    print("Message send")


def main(login, password, count_message):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.list()
     
    mail.select("inbox")
    
    result, data = mail.search(None, "ALL")
    index_list = data[0].split()
    results = index_list[-1]

    results = bytes(str(count_message + 1), encoding = 'utf-8')

    last_message_id = open("lastid.txt", "w")
    last_message_id.write(str(results.decode("utf-8")))
    last_message_id.close()

    result, data = mail.fetch(results, "(RFC822)")

    raw_email = data[0][1]

    email_message = email.message_from_string(raw_email.decode("utf-8"))

    from_user = email.utils.parseaddr(email_message['From'])[1]

    print(from_user)

    message(login, password, from_user)


def new_message():
    login = "azov485@gmail.com"
    password = "jenes85&"

    check_message(login, password)

    while True:
        last_message_id = open("lastid.txt", "r")
        result = last_message_id.read()
        result = int(result)
        
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(login, password)
            mail.list()
            mail.select("inbox")

        except:
            continue

        resultes, data = mail.search(None, "ALL")
        index_list = data[0].split()
        results = index_list[-1].decode("utf-8")
        results = int(results)

        if result < results:
            try:
                time.sleep(5)
                main(login, password, result)

            except:
                last_message_id = open("lastid.txt", "r")
                result = last_message_id.read()
                result = int(result)
                last_message_id.close()

                res = result - 1

                last_message_id = open("lastid.txt", "w")
                last_message_id.write(str(res))
                last_message_id.close()

new_message()
import requests
import smtplib
import time
from email.mime.text import MIMEText


def web_healthy(url):
    try:
        response = requests.head(url, timeout=5)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False


def send_email(subject, to_addr, body_text):
    msg = MIMEText(body_text, "plain")
    msg['Subject'] = subject
    msg['From'] = from_addr

    # These settings are tightly configured for yandex mail, but might also work with gmail and other services
    server = smtplib.SMTP(host, 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print("Successfully sent the mail")


url = ""  # URL of needed web service. Must be written in this format: example.com

# Mail variables

host = 'smtp.yandex.com'
from_addr = ''
username = ''
password = ''
subject = url + " is down!!!"
to_addr = ''
body_text = """\
Web service is down. Take responsibility for your actions -_-
"""

# The logic of script

while True:
    time.sleep(60)
    if web_healthy(url):
        print('Web service is up')
        loop = False
        while not loop:
            if not web_healthy(url):
                loop = True
    else:
        print('Web service is down')
        loop = False
        send_email(subject, to_addr, body_text)
        while not loop:
            if web_healthy(url):
                loop = True

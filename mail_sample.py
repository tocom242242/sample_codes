import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import configparser

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')


FROM_ADDRESS = config.get("mail", "mail_address1")
MY_PASSWORD = config.get("mail", "password")
TO_ADDRESS = config.get("mail", "mail_address2")
SUBJECT = 'test'
BODY = 'test'


def create_message(from_addr, to_addr,  subject, body):
    """
        メッセージを作成する 
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, msg):
    """
        メッセージを送る 
    """
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = BODY

    msg = create_message(FROM_ADDRESS, to_addr, subject, body)
    send(FROM_ADDRESS, to_addr, msg)

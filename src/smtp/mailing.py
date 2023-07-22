import smtplib
from email.mime.text import MIMEText

from envs import Envs


class Mailing:
    def __init__(self):
        self.__sender = Envs.EMAIL_ACCOUNT.value
        self.__password = Envs.EMAIL_PASSWORD.value
        self.__title = 'New deal is created on https://sale.capital/'

    @staticmethod
    def __generate_recipients():
        return ["iwilly17@gmail.com"]

    @staticmethod
    def __generate_subject():
        return "New deal is created on bitrix"

    def send_email(self):
        msg = MIMEText(self.__title)
        msg['Subject'] = self.__generate_subject()
        msg['From'] = self.__sender
        msg['To'] = ', '.join(self.__generate_recipients())
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.__sender, self.__password)
                smtp_server.sendmail(self.__sender, self.__generate_recipients(),   msg.as_string())
        except Exception as e:
            print('error', e)


mailing = Mailing()

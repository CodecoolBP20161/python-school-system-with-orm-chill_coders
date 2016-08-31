from connection import Connection
import smtplib


class EmailSender(object):
    """Handles email transactions."""

    def __init__(self, email_receiver, text, email_address, email_password):
        self.email_receiver = email_receiver
        self.text = text
        self.email_address = email_address
        self.email_password = email_password

    def sending(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_address, self.email_password)

        msg = self.text
        server.sendmail(self.email_address, self.email_receiver, msg.encode('UTF-8'))
        print('Email\'s been sent...')
        server.quit()
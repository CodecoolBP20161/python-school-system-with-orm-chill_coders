import smtplib
import getpass

my_email_address = "testerzh1234@gmail.com"

PASSWORD = getpass.getpass('Please, enter your email password: ')


class EmailSender(object):
    """Handles email transactions."""

    def __init__(self, email_receiver, text):
        self.email_receiver = email_receiver
        self.text = text
        self.password = PASSWORD
        self.email_sender = my_email_address

    def sending(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_sender, self.password)

        msg = self.text
        server.sendmail(self.email_sender, self.email_receiver, msg.encode('UTF-8'))
        print('Email\'s been sent...')
        server.quit()
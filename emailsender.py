from connection import Connection
import smtplib


class EmailSender(object):
    """Handles email transactions."""

    def __init__(self, email_receiver, email_address, email_password, specialisation):
        self.email_receiver = email_receiver
        self.email_address = email_address
        self.email_password = email_password
        self.specialisation = specialisation

    def create_email_text(self, option):
        if option == 'applicant_interview_email':
            message = """
                                Dear {0}!

                                The next step in your Codecool application process is
                                just on your doorstep!
                                We have scheduled an interview slot for your.

                                Details:

                                Location: {1}
                                Related mentor's name: {2}
                                Date: {3}
                                Time/start: {4}
                                Time/end: {5}

                                We're really looking forward to meeting with you!

                                Yours sincerely,
                                CC Staff
                                """.format(*self.specialisation)

        elif option == 'applicant_start_email':
                                message = """
                                Dear {0}!

                                We gladly received your application. First of all, we have
                                generated a personal application code for you. Here it is:
                                {1}.

                                If everything goes fine with your application process,
                                you're going to be informed about your interview's details
                                soon.

                                One thing for sure, it is probably going to be held in {2}.

                                We're looking forward to meeting with you!

                                Yours sincerely,
                                CC Staff
                                """.format(*self.specialisation)

        return message

    def sending(self, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_address, self.email_password)

        msg = message
        server.sendmail(self.email_address, self.email_receiver, msg.encode('UTF-8'))
        print('Email\'s been sent...')
        server.quit()

    def end_of_sending_process(self):
        print("{0}\'s just received an interview slot.".format(self.specialisation[0]))
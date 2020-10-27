import smtplib
import ssl
import os


class MailSender:

    def __init__(self, smtp_server=None, sender_email=None, password=None, receiver_email=None):
        self.port = 465
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER")
        self.sender_email = sender_email or os.getenv("SENDER_MAIL")
        self.password = password or os.getenv("MAIL_PASSWORD")
        self.receiver_email = receiver_email or os.getenv("RECEIVER_MAIL")

    def send_mail(self, subject=None, message=None):
        mail = f"""\
        Subject: {subject}
        
        {message}
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, mail)

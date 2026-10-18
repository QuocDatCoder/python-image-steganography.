import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    @staticmethod
    def send_key_mail(sender_email, sender_password, receiver_email, secret_key):
        """Sends the secret key to the receiver's email."""
        subject = "Secret Key for Image Steganography"
        body = f"Hello,\n\nThe secret key for the stego-protected file is: {secret_key}\n\nUse this key to decode the hidden message."
        
        try:
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

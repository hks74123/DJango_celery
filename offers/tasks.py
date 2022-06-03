from celery import shared_task
import smtplib
from email.message import EmailMessage  
from django.conf import settings
from django.contrib.auth.models import User 
from .models import *

def send_mail_to_users(to,title,validity):
        # logic to send mail to user
    sender_mail = f"{settings.MAIL_SENDER}"
    password_sender = f"{settings.PASS_MAIL}"
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender_mail
    message['Subject'] = "Welcome to Django-Celery"
    message.set_content(
        f"Hello User we have a new offer for you \n  title:{title} and valid till:{validity} \nvalid for next 15 minutes.")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         # success 
    except:
        return False 



@shared_task(bind=True)
def send_mail(self):
    offer_obj = offers.objects.order_by('-id')[0]
    title = offer_obj.title
    validity = offer_obj.end - offer_obj.start
    users = User.objects.all()
    for user in users:
        send_mail_to_users(user.email,title,validity)
    return "Done"
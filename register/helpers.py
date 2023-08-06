
from django.core.mail import send_mail
from django.conf import settings
import uuid


def send_forget_password_mail(email,token):

    subject = 'Your Forget Password Link'

    message = f'Click the below link to change the password http://127.0.0.1:8000/change_password/{token}/'

    email_from = settings.EMAIL_HOST_USER

    receipient_list = [email]

    send_mail(subject,message,email_from,receipient_list)

    return True
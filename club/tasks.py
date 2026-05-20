# club/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from twilio.rest import Client


@shared_task
def send_sms_and_email_task(phone_number, text, recipient_email):
    # Отправка SMS через Twilio
    account_sid = 'YOUR_TWILIO_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    sms = client.messages.create(
        body=text,
        from_='+1234567890',
        to=phone_number
    )

    # Отправка Email
    send_mail(
        subject='Новое SMS сообщение',
        message=f'Вы получили SMS: {text}',
        from_email=None,  # берется DEFAULT_FROM_EMAIL
        recipient_list=[recipient_email],
        fail_silently=False,
    )

    return sms.sid
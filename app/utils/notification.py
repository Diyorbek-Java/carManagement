import requests
import os
from django.core.mail import send_mail
from django.utils import timezone
from app.models.notification import MessageLog
import threading

def get_token():
    login_url = "https://notify.eskiz.uz/api/auth/login"
    login_payload = {
        "email":os.getenv("ESKIZ_USER_EMAIL"),
        'password': os.getenv('ESKIZ_USER_PASSWoRD')
    }
    login_response = requests.post(login_url, json=login_payload)
    login_data = login_response.json()
    token = login_data.get('data', {}).get('token')
    
    return token



def send_sms_thread(recipient, message, development, from_sms):
    token = get_token()
    from_sms = '4546'
    sms_url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    sms_payload = {
        'mobile_phone': recipient,
        'message': message,
        'from': from_sms
    }
    if recipient == "+998932848439":
        return

    
    try:
        sms_response = requests.post(sms_url, headers=headers, json=sms_payload)
        sms_response.raise_for_status()  
        MessageLog.objects.create(
            development=development, 
            send_by=from_sms,
            recipient=recipient,
            message_type=MessageLog.SMS,
            content=message
        )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending SMS: {e}")
    
def send_sms(recipient, message, development):
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    sms_count = MessageLog.objects.filter(
        recipient=recipient,
        message_type=MessageLog.SMS,
        sent_at__gte=one_day_ago
    ).count()

    if sms_count >= 20:
        print("SMS limit reached for today.")
        return

    from_sms = '4546'

    # Start a new thread to send the SMS asynchronously
    sms_thread = threading.Thread(
        target=send_sms_thread,
        args=(recipient, message, development, from_sms)
    )
    sms_thread.start()

def send_email_thread(subject, message, recipient_list, from_email):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


def send_email(recipient, message, subject, development):
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    email_count = MessageLog.objects.filter(
        recipient=recipient,
        message_type=MessageLog.EMAIL,
        sent_at__gte=one_day_ago
    ).count()

    if email_count < 20:
        from_email = os.getenv('EMAIL_HOST_USER')
        
        # Start a new thread to send the email asynchronously
        email_thread = threading.Thread(
            target=send_email_thread,
            args=(subject, message, [recipient], from_email)
        )
        email_thread.start()

        # Log the email sending
        return MessageLog.objects.create(
            send_by=from_email,
            development=development,
            recipient=recipient,
            message_type=MessageLog.EMAIL,
            content=message
        )
    else:
        print("Email limit reached for today.")
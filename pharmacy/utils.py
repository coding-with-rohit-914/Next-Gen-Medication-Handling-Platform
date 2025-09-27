import requests
from django.conf import settings
from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP is: {otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


#Fast2SMS
'''
def send_otp_sms(phone, otp):
    api_key = settings.FAST2SMS_API_KEY
    url = f"https://www.fast2sms.com/dev/bulkV2"
    data = {
        'variables_values': otp,
        'route': 'otp',
        'numbers': phone,
    }
    headers = {
        'authorization': api_key,
        'Content-Type': "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=data, headers=headers)
    print("SMS SENT", response.text)
'''

'''
#Twilio SMS

from twilio.rest import Client

def send_otp_sms(phone, otp):
    account_sid = 'your_twilio_sid'
    auth_token = 'your_twilio_token'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_='+1234567890',
        to=f'+91{phone}'
    )
    print(message.sid)
'''
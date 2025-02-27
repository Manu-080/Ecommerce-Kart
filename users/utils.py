import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate 6-digit OTP

def send_otp_email(email, otp):
    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

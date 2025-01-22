import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel

def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email, token, user_type=None):
    subject = "Verify your email address"
    message = f"""
                Hi, Please verify your email account by clicking this link
                http://127.0.0.1:8000/accounts/verify-account/{token}{f'/{user_type}/' if user_type else ''}
                """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def sendOTPtoEmail(email, otp):
    subject = "OTP for Account login"
    message = f"""
                Hi, Please use this OTP for login
                
                {otp}
                """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

# to generate unique slug
def generateSlug(hotel_name):
    slug = slugify(hotel_name) +'-'+ str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generateSlug(hotel_name)
    return slug




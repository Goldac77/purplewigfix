import random, string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.senders.accounts import *
from core.retrievers.accounts import *

from core.models import *
def generate_otp(otp_length):
    """
    Generate a one time pin with specified length
    """

    return "".join([random.choice(string.digits) for i in range(otp_length)])


def email_verification(email: str, otp_length: int):
    """
    Send email verification code to new user
    """

    subject = "Purple Wig  Email Verification Code"
    pin = generate_otp(otp_length)
    print(f"{pin}")

    sender = "info@successbuilderhub.com"
    receiver = [email]
    html_content = render_to_string(
        "core/verification_email.html",
        {"pin": pin, "receiver": email},
    )
    text_content = strip_tags(html_content)
    email_obj = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email_obj.attach_alternative(html_content, "text/html")

    if email_obj.send():
        token = get_verification_token(receiver)
        if token:
            update_verification_token(token, pin)
        else:
            print(f"receiver: {receiver}")
            pin_created = create_verification_token(receiver, pin)
            print(f"pin created: {pin_created}")
        return True
    return False


def verification_confirmation_email(email):
    """
    Confirm email address verification
    """
    subject = "Purple Wig Email Address Verification Confirmation"

    sender = "info@successbuilderhub.com"
    receiver = [email]

    html_content = render_to_string(
        "core/verification_confirmation.html",
        {"receiver": receiver},
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
    email.attach_alternative(html_content, "text/html")

    if email.send():
        return True
    return False

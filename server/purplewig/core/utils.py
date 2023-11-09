import random
from django.core.mail import EmailMultiAlternatives, send_mail
from core.senders import *
from core.retrievers import *

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

    sender = "purplewig@gamil.com"
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
            create_verification_token(receiver, pin)
        return True
    return False


def verification_confirmation_email(email):
    """
    Confirm email address verification
    """
    subject = "Purple Wig Email Address Verification Confirmation"

    sender = "purplewig@gmail.com"
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

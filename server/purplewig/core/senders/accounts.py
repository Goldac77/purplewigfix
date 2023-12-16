from django.contrib.auth import get_user_model
from core.models import PurpleWigUser, VerificationToken, PasswordResetToken
from core.serializers import PurpleWigUserSerializer
import pytz
from datetime import datetime, timedelta, timezone

UTC = pytz.UTC

UserModel = get_user_model()

def create_user(email, password):
    """Create user"""
    user = UserModel.objects.create_user(email=email, password=password)
    return user


def create_verification_token(email, token):
    """Create verification token"""
    time_generated = UTC.localize(datetime.now())
    verification_token = VerificationToken.objects.create(email=email, token=token, time=time_generated)
    return verification_token


def update_verification_token(verification_token, token):
    """Update verification token"""
    time_generated = UTC.localize(datetime.now())
    verification_token.token = token
    verification_token.time = time_generated
    verification_token.save()
    return verification_token

def create_password_token(email, token):
    """Create password token"""
    time_generated = UTC.localize(datetime.now())
    password_token = PasswordResetToken.objects.create(email=email, token=token, time=time_generated)
    return password_token


def update_password_token(password_token, token):
    """Update password token"""
    time_generated = UTC.localize(datetime.now())
    password_token.token = token
    password_token.time = time_generated
    password_token.save()
    return password_token
from core.models import *
from core.serializers import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def get_user_information(user):
    """Get user information"""
    user_information = {
        "id": user.id,
        "email": user.email,
    }
    return user_information


def get_user_by_email(email):
    """retrieve a user by email Get user by email"""
    try:
        user = PurpleWigUser.objects.get(email=email)
        return user
    except PurpleWigUser.DoesNotExist:
        return None


def get_all_users():
    """Get all objects from purplewig"""
    queryset = PurpleWigUser.objects.all()
    serializer = PurpleWigUserSerializer(queryset, many=True)
    return serializer.data


def get_verification_token(email):
    """Get verification token"""
    try:
        token = VerificationToken.objects.get(email=email)
        return token
    except VerificationToken.DoesNotExist:
        return None
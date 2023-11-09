from core.models import PurpleWigUser, VerificationToken
from rest_framework import serializers



class PurpleWigUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurpleWigUser
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class VerificationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationToken
        fields = ["token", "email"]
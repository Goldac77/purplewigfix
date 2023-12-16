from core.models import *
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
        
        
class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"
        

class CourseRegistrationSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:
        model = CourseRegistration
        fields = ["email", "full_name", "phone_number", "gender", "course"]

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"
        
class ServiceRegistrationSerializer(serializers.ModelSerializer):

    service = ServiceSerializer()
    class Meta:
        model = ServiceRegistration
        fields = ["email", "full_name", "phone_number", "gender",'additional_info', "service"]
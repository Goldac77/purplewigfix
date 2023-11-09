from django.shortcuts import render
from core.models import PurpleWigUser
from core.serializers import PurpleWigUserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from core.senders.accounts import *
from core.retrievers.accounts import *
from core.utils import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import threading


class AccountCreation(viewsets.ViewSet):
    """Create account"""
    def list(self, request):
        """Get all users"""
        users = get_all_users()
        context = {"users": users}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        email = request.data['email']
        password = request.data['password']
        user = get_user_by_email(email=email)
        
        if not email or password:
            context = {"detail": "Email and password are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        if user:
            context = {"detail" :"User already exists"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        user = create_user(email, password)
        email_thread = threading.Thread(target=email_verification, args=[email, 5])
        email_thread.start()
        context = {"detail": "Account created successfully", "user": get_user_information(user)}
        return Response(context, status=status.HTTP_201_CREATED)

    
    def send_confirmation_email(self, request):
        """Send confirmation email"""
        email = request.data['email']
        user = get_user_by_email(email=email)
        if user.verified:
            context = {"detail": "User already verified"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        if not email:
            context = {"detail": "Email is required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user_otp = get_verification_token(email)
        if user_otp:
            user_otp.delete()
            
        if email_verification(email, 6):
            context = {"detail": "Verification code successfully sent", "email": email}
            return Response(context, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not send verification code"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    
    def verify_account(self, request):
        """Verify account"""
        email = request.data['email']
        otp = request.data['otp']
        user = get_user_by_email(email=email)
        
        if not email or otp:
            context = {"detail": "Email and otp are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if user.verified:
            context = {"detail": "User already verified"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        user_otp = get_verification_token(email)
        if otp == user_otp.token:
            if user_otp.time + timedelta(minutes=5) < datetime.now():
                user.verified = True
                user.save()
                email_thread = threading.Thread(target=verification_confirmation_email, args=[email])
                context = {"detail": "Account verified successfully", "user": get_user_information(user)}
                return Response(context, status=status.HTTP_200_OK)
            else:
                user_otp.delete()
                context = {"detail": "Verification code expired"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {"detail": "Invalid verification code"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
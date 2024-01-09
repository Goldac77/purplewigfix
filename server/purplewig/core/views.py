from django.shortcuts import render
from core.models import *
from core.serializers import PurpleWigUserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from core.senders.accounts import *
from core.retrievers.accounts import *
from core.retrievers.course import *
from core.senders.course import *
from core.utils import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import threading
from datetime import datetime, timedelta, timezone
import pytz
UTC = pytz.UTC
import os
import requests


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
        # print(f"email: {email}, password: {password}")
        
        if email is None or password is None:
            print(f"email: {email}, password: {password}")

            context = {"detail": "Email and password are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user = get_user_by_email(email=email)

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
            
        if email_verification(email, 5):
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
        
        if not email or not otp:
            context = {"detail": "Email and otp are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if user.verified:
            context = {"detail": "User already verified"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        user_otp = get_verification_token(email)
        if otp == user_otp.token:
            if user_otp.time + timedelta(minutes=5) > datetime.now(timezone.utc):
                user.verified = True
                user.save()
                user_otp.delete()
                email_thread = threading.Thread(target=verification_confirmation_email, args=[email])
                context = {"detail": "Account verified successfully", "user": get_user_information(user)}
                return Response(context, status=status.HTTP_200_OK)
            else:
                user_otp.delete()
                context = {"detail": "Verification code expired"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {"detail": "Invalid verification code"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetViewset(viewsets.ViewSet):
    """Password rest viewset"""
    
    def password_reset_request(self, request):
        """Password reset"""
        email = request.data['email']
        if not email:
            context = {"detail": "Email is required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user = get_user_by_email(email=email)
        if not user:
            context = {"detail": "User does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        user_otp = get_password_reset_token(email)
        if user_otp:
            user_otp.delete()
        if password_reset_verification(email, 5):
            context = {"detail": "Password reset code successfully sent", "email": email}
            return Response(context, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not send password reset code"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    def password_reset_confirm(self, request):
        """Password set"""
        email = request.data['email']
        otp = request.data['otp']
        password = request.data['password']
        user = get_user_by_email(email=email)
        if not email or not otp or not password:
            context = {"detail": "Email, otp and password are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user_otp = get_password_reset_token(email)
        if otp == user_otp.token:
            if user_otp.time + timedelta(minutes=5) > datetime.now(timezone.utc):
                user.set_password(password)
                user.save()
                user_otp.delete()
                context = {"detail": "Password reset successfully"}
                return Response(context, status=status.HTTP_200_OK)
            else:
                user_otp.delete()
                context = {"detail": "Password reset code expired"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {"detail": "Invalid password reset code"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class CourseViewset(viewsets.ViewSet):
    """Course viewset"""
    
    def list(self, request):
        """Get all courses"""
        courses = get_all_courses()
        context = {"courses": courses}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        """Create course"""
        name = request.data['name']
        description = request.data['description']
        if not name or not description:
            context = {"detail": "Name and description are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        course = get_course_by_name(name)
        if course:
            context = {"detail": "Course already exists"}
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        course = create_course(name, description)
        context = {"detail": "Course created successfully", "course": get_course_information(course)}
        return Response(context, status=status.HTTP_201_CREATED)
    
    
    def retrieve(self, request, pk=None):
        """Get course by id"""
        course = get_course_by_id(pk)
        if not course:
            context = {"detail": "Course does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        context = {"course": get_course_information(course)}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def update(self, request, pk=None):
        """Update course"""
        name = request.data['name']
        description = request.data['description']
        if not name or not description:
            context = {"detail": "Name and description are required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        course = get_course_by_id(pk)
        if not course:
            context = {"detail": "Course does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        course = update_course(course, name, description)
        context = {"detail": "Course updated successfully", "course": get_course_information(course)}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk=None):
        """Delete course"""
        course = get_course_by_id(pk)
        if not course:
            context = {"detail": "Course does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        context = {"detail": "Course deleted successfully"}
        return
    

class CourseRegistrationViewset(viewsets.ViewSet):
    """Register course viewset"""
    
    def create(self, request, id):
        """Register course"""
        course = get_course_by_id(id)
        if not course:
            context = {"detail": "Course does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        course_registration = create_course_registration(course, request.data)
        context = {"detail": "Course registration successful", "course_registration": course_registration}
        return Response(context, status=status.HTTP_201_CREATED)
    
    
    def list(self, request):
        """Get all course registrations"""
        course_registrations = get_all_course_registrations()
        context = {"course_registrations": course_registrations}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        """Get course registration by id"""
        course_registration = get_course_registration_by_id(pk)
        if not course_registration:
            context = {"detail": "Course registration does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        context = {"course_registration": course_registration}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk=None):
        """Delete course registration"""
        course_registration = get_course_registration_by_id(pk)
        if not course_registration:
            context = {"detail": "Course registration does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        course_registration.delete()
        context = {"detail": "Course registration deleted successfully"}
        return Response(context, status=status.HTTP_200_OK)
    
    
    def update(self, request, pk=None):
        """Update course registration"""
        course_registration = get_course_registration_by_id(pk)
        if not course_registration:
            context = {"detail": "Course registration does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

class ServiceRegistrationViewset(viewsets.ViewSet):
    """Register course viewset"""
    
    def create(self, request, id):
        """Register course"""
        service = get_service_by_id(id)
        SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
        url="https://api.paystack.co/transaction/initialize"
        email = request.data.get('email')
        if not service:
            context = {"detail": "service does not exist"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        print(service.price)
        if service:
            data = {
                "email": email,
                "amount": str(service.price * 100),
                "currency": 'GHS'
            }
            headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=response.status_code)
            else:
                return Response(response.text, status=response.status_code)
    
    
    def verify_transaction(self, request)-> Response:
        """ endpoint to verify transaction

        Args:
            request (http request): http request object
            Return (http response): http response object
        """
        
        SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
        service_id = request.data.get('service_id')
        reference = request.data.get('reference')
        email = request.data.get('email')


        if not service_id:
            context = {
                "error": "service id is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if not reference:
            context = {
                "error": "reference is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        
        headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json"
            }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response = response.json()
            if response["data"]["status"] == "success":
                service = get_service_by_id(service_id)
                user_service = create_service_registration(service, request.data)
                
                Transaction.objects.create(email=email, amount=service.price)
                context = {
                    "detail": "Service booked successfully",
                    "data": user_service
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "detail": "Transaction failed"
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response.text, status=response.status_code)        
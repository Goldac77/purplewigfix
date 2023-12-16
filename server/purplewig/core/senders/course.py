from core.models import Course, CourseRegistration, Service, ServiceRegistration
from core.serializers import CourseSerializer, CourseRegistrationSerializer, ServiceRegistrationSerializer

def create_course(title, description, price, image):
    """Create course"""
    course = Course.objects.create(title=title, description=description, price=price, image=image)
    return course


def update_course(course, title, description, price, image):
    """Update course"""
    course.title = title
    course.description = description
    course.price = price
    course.image = image
    course.save()
    return course

def create_course_registration(course, data):
    """Create course registration"""
    email = data['email']
    full_name = data['full_name']
    phone_number = data['phone_number']
    gender = data['gender']
    course_register = CourseRegistration(email=email, full_name=full_name, phone_number=phone_number, course=course, gender=gender)
    course_registration_serializer = CourseRegistrationSerializer(course_register)
    
    return course_registration_serializer.data



def create_service_registration(service, data):
    """Create course registration"""
    email = data['email']
    full_name = data['full_name']
    phone_number = data['phone_number']
    gender = data['gender']
    additional_info = data['additional_info']
    service_register = ServiceRegistration(email=email, full_name=full_name, phone_number=phone_number, service=service, gender=gender, additional_info=additional_info)
    service_registration_serializer = ServiceRegistrationSerializer(service_register)
    
    return service_registration_serializer.data

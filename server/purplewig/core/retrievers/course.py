from core.models import Course, Service
from core.serializers import CourseSerializer

def get_courses():
    """Get all courses"""
    courses = Course.objects.all()
    serialiazer = CourseSerializer(courses, many=True)
    return serialiazer.data

def get_course_by_id(course_id):
    """Get course by id"""
    course = Course.objects.get(pk=course_id)
    return course

def get_course_by_title(course_title):
    """Get course by title"""
    course = Course.objects.get(title=course_title)
    return course


def get_course_information(course_id):
    """Get course information"""
    course = get_course_by_id(course_id)
    serializer = CourseSerializer(course)
    return serializer.data


def get_service_by_id(id):
    """get service by id

    Args:
        id (int): service id
    """
    service = Service.objects.get(pk=id)
    return service
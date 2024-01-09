from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import uuid



GENDER = [
    ("male", "Male"),
    ("female", "Female")
]
class PurpleWigBaseUser(BaseUserManager):
    """Create base user"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create super user"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser=True")
        self.create_user(email, password, **extra_fields)


class PurpleWigUser(AbstractBaseUser):
    """PurpleWigBaseUser model"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = PurpleWigBaseUser()
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    
    def __str__(self):
        return self.email

class VerificationToken(models.Model):
    """Verification token model"""
    token = models.CharField(max_length=255)
    email = models.EmailField()
    time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.email} - {self.token}"
    


class PasswordResetToken(models.Model):
    """Password reset token model"""
    token = models.CharField(max_length=255)
    email = models.EmailField()
    time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.email} - {self.token}"
    
    
    

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses')
    
    def __str__(self):
        return self.title
    

class CourseRegistration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.email} - {self.course.title}"
    
    

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services')
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class ServiceRegistration(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    additional_info = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.service.title}"
    

class Transaction(models.Model):
    email = models.EmailField(max_length=254)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.email} - {self.amount}"
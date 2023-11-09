from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

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
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
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
    time = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator
from django.db import models
from course.models import Course
from .managers import CustomUserManager

class BaseUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Student', 'Student')])
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    hour_rate = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(30)])
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    objects = CustomUserManager()

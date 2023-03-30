from datetime import datetime, timedelta

import jwt
from course.models import Course, Program
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from helpers.models import TrackingModel
from PIL import Image

# LEVEL_COURSE = "Level course"
BEGINNER = "Beginner"
INTERMEDIATE = "Intermediate"
ADVANCED = "Advanced"

LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BEGINNER, "Beginner"),
    (INTERMEDIATE, "Intermediate"),
    (ADVANCED, "Advanced")
)

GENDER = (('M', 'Male'), ('F', 'Female'))
LEARNING_STYLES = [('visual', 'Visual'), ('auditory', 'Auditory'), ('kinesthetic', 'Kinesthetic')]


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Username field is required')
        
        if not email:
            raise ValueError('Email field is required')
        
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) | 
                         Q(first_name__icontains=query)| 
                         Q(last_name__icontains=query)| 
                         Q(email__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class User(AbstractUser, TrackingModel):
    email = models.EmailField(_('email address'), db_index=True, unique=True, blank=False, null=False)
    gender = models.CharField(max_length=10, choices=GENDER)
    phone = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', default='default.png', null=True)
    
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    
    newsletter = models.BooleanField(default=False)
    
    email_verified = models.BooleanField(_('email verified'), default=False, help_text='Designates whether this users email is verified.')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_student:
            return "Student"
        elif self.is_lecturer:
            return "Lecturer"

    def get_picture(self): 
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) | 
                         Q(department__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class TechSkill(TrackingModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title
    

class Student(TrackingModel):
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    # program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    goals = models.TextField(blank=True, null=True)
    learning_style = models.CharField(choices=LEARNING_STYLES, max_length=50)
    availability = models.CharField(max_length=50, blank=True, null=True)   
    tech_skills = models.ManyToManyField(TechSkill, related_name='tech_skills', blank=True)
    projects = models.ManyToManyField(Project, related_name='projects', blank=True)
    
    objects = StudentManager()

    def __str__(self):
        return self.student.get_full_name

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)


class Lecturer(TrackingModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer')
    credentials = models.TextField()
    teaching_experience = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.user.get_full_name

    # should get this working asap
    # def get_courses(self):
    #     return Course.objects.filter(courseallocation__lecturer=self)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.student.get_full_name

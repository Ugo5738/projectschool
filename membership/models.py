from accounts.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from helpers.models import TrackingModel
from project.models import Project, TechSkill

LEARNING_STYLES = [('visual', 'Visual'), ('auditory', 'Auditory'), ('kinesthetic', 'Kinesthetic')]

# need to finetune this
class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) | 
                         Q(department__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs
    

class Student(TrackingModel):
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
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


class Instructor(TrackingModel):
    instructor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile'
    )
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.instructor.get_full_name
    
    def get_absolute_url(self):
        return reverse('instructor_profile', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.instructor.delete()
        super().delete(*args, **kwargs)


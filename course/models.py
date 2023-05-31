from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from helpers.models import TrackingModel
from membership.models import Instructor, Student
from project.models import Project, TechSkill

LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

TYPE_CHOICES = (
        ('V', 'Video'),
        ('D', 'Document'),
    )
    

class ProgramManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Program(TrackingModel):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='program_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.PositiveIntegerField(help_text='Duration in weeks')
    
    objects = ProgramManager()

    def __str__(self):
        return self.title
    
    def get_short_description(self):
        return self.description[:500]


class CourseManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)|  
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class CourseMetadata(models.Model):
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    certificate = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Course metadata'


class CourseContent(models.Model):
    syllabus = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Course content'


class CourseDetails(models.Model):
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    duration = models.PositiveIntegerField(default=12)
    enrollment_count = models.PositiveIntegerField(default=0)
    enrollment_deadline = models.DateField(null=True, blank=True)

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    skills = models.ManyToManyField(TechSkill)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)  # I am not sure this is needed
    
    class Meta:
        verbose_name_plural = 'Course details'


class Course(TrackingModel):
    title = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    
    metadata = models.OneToOneField(CourseMetadata, on_delete=models.CASCADE)
    content = models.OneToOneField(CourseContent, on_delete=models.CASCADE)
    details = models.OneToOneField(CourseDetails, on_delete=models.CASCADE)
    
    objects = CourseManager()

    def __str__(self):
        return f"{self.title}"
    
    def get_short_description(self):
        return f"{self.description[:200]}..."


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.TextField()
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Module(TrackingModel):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Lesson(TrackingModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Video(TrackingModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(
        upload_to='videos/', 
        validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])],
        null=True, 
        blank=True,
    )

    def __str__(self):
        return self.title
    

class File(TrackingModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to='files/', 
        validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])],
        null=True, 
        blank=True,
    )

    def __str__(self):
        return self.title

        
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course', 'program',)

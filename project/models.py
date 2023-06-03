from datetime import date

from accounts.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from helpers.models import TrackingModel

STATUS_CHOICES = [
        ('new', 'New'),
        ('completed', 'Completed'),
    ]


class TechSkill(TrackingModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='new', choices=STATUS_CHOICES)
    start_date = models.DateField(default=date.today)  # default=timezone.now().date)
    duration = models.PositiveIntegerField(default=12)  # duration in weeks
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # this is also the client
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_projects', null=True, blank=True)
    paid = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # client = models.CharField(max_length=100, null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    attachments = models.ManyToManyField('ProjectAttachment', blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(weeks=self.duration)
        super().save(*args, **kwargs)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")
    

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    due_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)


class ProjectAttachment(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='project_attachments/', 
        validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])], 
        null=True, 
        blank=True,
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    comments = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Activity(TrackingModel):
    ACTIVITY_CHOICES = [
        ('created_project', 'Created a new project'),
        ('updated_project', 'Updated a project'),
        ('deleted_project', 'Deleted a project'),
        ('created_task', 'Created a new task'),
        ('updated_task', 'Updated a task'),
        ('deleted_task', 'Deleted a task'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        if self.project:
            return f"{self.user.first_name} {self.activity_type} '{self.project.title}'"
        elif self.task:
            return f"{self.user.first_name} {self.activity_type} '{self.task.title}'"
        else:
            return f"{self.user.first_name} {self.activity_type}"
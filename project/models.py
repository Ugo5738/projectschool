from django.db import models
from helpers.models import TrackingModel


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


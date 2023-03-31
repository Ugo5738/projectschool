from datetime import date, timedelta

from django.db import models
from helpers.models import TrackingModel


class TechSkill(TrackingModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=date.today)
    duration = models.PositiveIntegerField(default=12)  # duration in weeks
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(days=self.duration)
        super().save(*args, **kwargs)


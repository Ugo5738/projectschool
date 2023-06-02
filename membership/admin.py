from django.contrib import admin
from membership import models

admin.site.register(models.Student)
admin.site.register(models.Instructor)
admin.site.register(models.Client)
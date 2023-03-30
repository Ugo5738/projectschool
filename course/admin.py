from course import models
from django.contrib import admin

admin.site.register(models.Program)
admin.site.register(models.Course)
admin.site.register(models.CourseAllocation)
admin.site.register(models.Upload)
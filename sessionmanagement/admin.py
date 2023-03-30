from django.contrib import admin

from .models import NewsAndEvents, Semester, Session

admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(NewsAndEvents)

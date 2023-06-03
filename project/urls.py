from django.urls import include, path
from project.views import (ActivityViewSet, ProjectAttachmentViewSet,
                           ProjectViewSet, TagViewSet, TaskViewSet,
                           TechSkillViewSet)
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-attachments', ProjectAttachmentViewSet, basename='projectattachment')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'techskills', TechSkillViewSet, basename='tech_skill')
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]

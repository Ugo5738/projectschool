from accounts.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from project.models import (Activity, Project, ProjectAttachment, Tag, Task,
                            TechSkill)
from project.serializers import (ActivitySerializer,
                                 ProjectAttachmentSerializer,
                                 ProjectSerializer, TagSerializer,
                                 TaskSerializer, TechSkillSerializer)
from rest_framework import filters, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed, edited and searched.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id', 'status']
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class ProjectAttachmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows project attachments to be viewed, edited and searched.
    """
    queryset = ProjectAttachment.objects.all()
    serializer_class = ProjectAttachmentSerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed, edited and searched.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed, edited and searched.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class TechSkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tech skills to be viewed, edited and searched.
    """
    queryset = TechSkill.objects.all()
    serializer_class = TechSkillSerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows activities to be viewed, edited and searched.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']

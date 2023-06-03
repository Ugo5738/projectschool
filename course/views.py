from accounts.pagination import CustomPageNumberPagination
from course.models import (Answer, Course, Enrollment, File, Lesson, Module,
                           Program, Question, Quiz, Video)
from course.serializers import (AnswerSerializer, CourseSerializer,
                                EnrollmentSerializer, FileSerializer,
                                LessonSerializer, ModuleSerializer,
                                ProgramSerializer, QuestionSerializer,
                                QuizSerializer, VideoSerializer)
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows programs to be viewed, edited and searched.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs
    

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quizes to be viewed or edited.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['id']


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows answers to be viewed or edited.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering = ['id']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']
    

class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows modules to be viewed or edited.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lessons to be created, viewed or edited.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be uploaded, viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be uploaded, viewed or edited.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows enrols to be created, viewed or edited.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']
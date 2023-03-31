from course.models import (Answer, Course, File, Lesson, Module, Program,
                           Question, Quiz, Video)
from course.serializers import (AnswerSerializer, CourseSerializer,
                                LessonSerializer, ModuleSerializer,
                                ProgramSerializer, QuestionSerializer,
                                QuizSerializer)
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows programs to be viewed, edited and searched.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quizes to be viewed or edited.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows answers to be viewed or edited.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows modules to be viewed or edited.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lessons to be viewed or edited.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VideoAPIView(APIView):
    def get(self, request, pk):
        video = Video.objects.get(pk=pk)
        file_url = request.build_absolute_uri(video.video_file.url)
        return Response({"url": file_url})


class FileAPIView(APIView):
    def get(self, request, pk):
        file = File.objects.get(pk=pk)
        file_url = request.build_absolute_uri(file.file.url)
        return Response({"url": file_url})
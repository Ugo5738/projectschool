from accounts.pagination import CustomPageNumberPagination
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from membership import serializers
from membership.models import Student
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response


class StudentAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.StudentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id']  # , 'student_profile', 'project', 'tech_skills']
    search_fields = ['id']  # , 'student', 'project', 'tech_skills']
    ordering_fields = ['id']  # , 'student', 'project', 'tech_skills']
    
    def perform_create(self, serializer):
        user = self.request.user
        user.is_student = True
        user.save()
        return serializer.save(student=user)
    
    def get_queryset(self):
        return Student.objects.all()
    

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'  # 'user_id'

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        user = self.request.user
        if not user.is_authenticated or not user.is_student:
            raise Http404
        return Student.objects.get(id=id)
        # return user.student use this when using user_id
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()


class InstructorAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.StudentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id']  # , 'student_profile', 'project', 'tech_skills']
    search_fields = ['id']  # , 'student', 'project', 'tech_skills']
    ordering_fields = ['id']  # , 'student', 'project', 'tech_skills']
    
    def perform_create(self, serializer):
        user = self.request.user
        user.is_student = True
        user.save()
        return serializer.save(student=user)
    
    def get_queryset(self):
        return Student.objects.all()
    

class InstructorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'  # 'user_id'

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        user = self.request.user
        if not user.is_authenticated or not user.is_student:
            raise Http404
        return Student.objects.get(id=id)
        # return user.student use this when using user_id
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

from accounts.pagination import CustomPageNumberPagination
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from membership import serializers
from membership.models import Client, Instructor, Referral, Student
from membership.serializers import (ClientSerializer, InstructorSerializer,
                                    ReferralSerializer, StudentSerializer)
from rest_framework import filters, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed, edited and searched.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class InstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instructors to be viewed, edited and searched.
    """
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed, edited and searched.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']


class ReferralViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows referrals to be viewed, edited and searched.
    """
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id']
    search_fields = ['id']
    ordering_fields = ['id']

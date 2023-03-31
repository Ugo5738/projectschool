from django.urls import path
from membership import views

urlpatterns = [
    path('student/', views.StudentAPIView.as_view(), name="student"),
    path('student/<int:id>/', views.StudentDetailAPIView.as_view(), name="student_detail"),
]
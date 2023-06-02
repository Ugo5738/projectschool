from django.urls import include, path
from membership import views
from rest_framework import routers

from .views import ClientViewSet, InstructorViewSet, StudentViewSet

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('student/', views.StudentAPIView.as_view(), name="student"),
#     path('student/<int:id>/', views.StudentDetailAPIView.as_view(), name="student_detail"),

#     path('instructor/', views.InstructorAPIView.as_view(), name="instructor"),
#     path('instructor/<int:id>/', views.InstructorDetailAPIView.as_view(), name="instructor_detail"),
# ]
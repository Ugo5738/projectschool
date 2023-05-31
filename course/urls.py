from course import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'programs', views.ProgramViewSet, basename='program')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'modules', views.ModuleViewSet, basename='module')
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'videos', views.VideoViewSet, basename='video')
router.register(r'files', views.FileViewSet, basename='file')
router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]

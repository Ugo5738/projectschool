from course import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'programs', views.ProgramViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'lessons', views.LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('videos/<int:pk>/', views.VideoAPIView.as_view()),
    path('files/<int:pk>/', views.FileAPIView.as_view()),
]

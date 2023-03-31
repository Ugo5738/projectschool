from accounts import views
from django.contrib.auth import views as auth_views
#########################
#########################
#########################
from django.urls import path, reverse_lazy
from rest_framework_simplejwt import views as jwt_views

from . import views

# urlpatterns = [
    # path("", views.IndexView.as_view(), name="home"),
    # path('signup/', views.SignupView.as_view(), name='signup'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page="index"), name='logout'),
    #################################################################################
    #################################################################################
    # path('students/', views.StudentListView.as_view(), name='student_list'),
    # path("student-add/", views.StudentAddView.as_view(), name="student_add"),
    # path('student/<int:pk>/edit/', views.EditStudentView.as_view(), name='student_edit'),
    # path('student/<int:pk>/delete/', views.DeleteStudentView.as_view(), name='student_delete'),
    #################################################################################
    #################################################################################

    #################################################################################
    #################################################################################   
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(
    #         template_name="accounts/password/password_reset.html",
    #         subject_template_name="accounts/password/password_reset_subject.txt",
    #         email_template_name="accounts/password/password_reset_email.html",
    #         from_email="webmaster@localhost",
    #         # success_url='/login/'
    #     ),
    #     name="password_reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(template_name="accounts/password/password_reset_done.html"),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset-confirm/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name="accounts/password/password_reset_confirm.html"
    #     ),
    #     name="password_reset_confirm",
    # ),
#     path(
#         "password-reset-complete/",
#         auth_views.PasswordResetCompleteView.as_view(
#             template_name="accounts/password/password_reset_complete.html"
#         ),
#         name="password_reset_complete",
#     ),
# ]


urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name='register'),
    # path('login', views.LoginAPIView.as_view(), name='login'),

    path('login/token/', jwt_views.TokenObtainPairView.as_view(), name='login_token'),
    path('login/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='login_token_refresh'),
    
    path('user/', views.UserListAPIView.as_view(), name="user_list"),
    path('user/<int:id>', views.UserDetailAPIView.as_view(), name="user_detail"),
]

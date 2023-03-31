from accounts import views
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name='register'),
    # path('login', views.LoginAPIView.as_view(), name='login'),

    path('login/token/', jwt_views.TokenObtainPairView.as_view(), name='login_token'),
    path('login/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='login_token_refresh'),
    
    # path('user/', views.UserListAPIView.as_view(), name="user_list"),
    # path('user/<int:id>', views.UserDetailAPIView.as_view(), name="user_detail"),
    path('', include(router.urls)),
]

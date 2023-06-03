from django.urls import include, path
from membership.views import (ClientViewSet, InstructorViewSet,
                              ReferralViewSet, StudentViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'referrals', ReferralViewSet, basename='referral')

urlpatterns = [
    path('', include(router.urls)),
]

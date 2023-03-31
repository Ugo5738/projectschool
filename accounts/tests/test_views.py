from accounts.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class StudentAPITestCase(APITestCase):
    def authenticate(self):
        response = self.client.post(reverse('register'), {
            "password": "testing",
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "gender": "M",
            "phone": "07033588400",
            "country": "Nigeria",
            "city": "Mile 2",
            "postal_code": "102102",
            "address": "Lagos",
            "newsletter": True,
            "is_student": True
        })
        user = User.objects.get(email=response.data["email"])
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)    

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    
    def create_student(self, user=False):
        sample_student = {
                'goals': 'learn python in 3 months', 
                'learning_style': 'visual',
                'availability': '4, 5, 6',
            }
        
        if user:
            user = User.objects.get(email="test@test.com")
            sample_student['student'] = user.id

        response = self.client.post(reverse('student'), sample_student)
        
        return response

from accounts.models import Project, Student, TechSkill, User
from django.urls import reverse
from rest_framework import status
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


class TestListCreateStudent(StudentAPITestCase):        
    def test_should_not_create_student_without_auth(self):
        response = self.create_student()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_student(self):
        self.authenticate()

        previous_student_count = Student.objects.all().count()        
        
        response = self.create_student(user=True)
        
        self.assertEqual(Student.objects.all().count(), previous_student_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student'], response.data['id'])
        self.assertEqual(response.data['goals'], 'learn python in 3 months')
        self.assertEqual(response.data['learning_style'], 'visual')
        self.assertEqual(response.data['availability'], '4, 5, 6')

    def test_retrieves_all_students(self):
        self.authenticate()
        response = self.client.get(reverse('student'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)


class TestStudentDetailAPIView(StudentAPITestCase):
    def test_retrieves_one_student_record(self):
        self.authenticate()

        student_response = self.create_student(user=True)

        response = self.client.get(reverse('student_detail', kwargs={'id': student_response.data['id']}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], student_response.data['id'])
        self.assertEqual(response.data['goals'], student_response.data['goals'])
        self.assertEqual(response.data['learning_style'], student_response.data['learning_style'])
        self.assertEqual(response.data['availability'], student_response.data['availability'])

    def test_updates_student_record(self):
        self.authenticate()

        student_response = self.create_student(user=True)

        data = {
            "goals": "learn javascript",
            "learning_style": "auditory"
        }
        
        response = self.client.patch(reverse('student_detail', kwargs={'id': student_response.data['id']}), data=data)
        updated_student = Student.objects.get(id=student_response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_student.goals, data['goals'])
        self.assertEqual(updated_student.learning_style, data['learning_style'])
    
    def test_students_tech_skill_project_connection(self):
        self.authenticate()
        student_response = self.create_student(user=True)

        tech_skill_1, created = TechSkill.objects.get_or_create(name='Python')
        tech_skill_2, created = TechSkill.objects.get_or_create(name='JavaScript')

        project_1, created = Project.objects.get_or_create(
            title='Webscrape Remote io',
            description='Get 10,000 jobs links',
            start_date='2023-04-01',
            end_date='2023-04-30'
        )
        project_2, created = Project.objects.get_or_create(
            title='Build a web app',
            description='Build a web app using Django and React',
            start_date='2023-05-01',
            end_date='2023-05-31'
        )
        
        # Make a PUT request to update the student instance with new tech_skills and projects
        data = {
            "tech_skills": [
                {"name": "Python"},
                {"name": "JavaScript"}
            ],
            "projects": [
                {"title": "Webscrape Remote io", "description": "Get 10,000 jobs links"},
                {"title": "Build a web app", "description": "Build a web app using Django and React"}
            ]
        }

        response = self.client.put(reverse('student_detail', kwargs={'id': student_response.data['id']}), data=data, format='json')
        response2 = self.client.patch(reverse('student_detail', kwargs={'id': student_response.data['id']}), data=data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
        # Check that the updated student instance has the expected tech_skills and projects
        updated_student = Student.objects.get(id=student_response.data['id'])

        self.assertIn(tech_skill_1, updated_student.tech_skills.all())
        self.assertIn(tech_skill_2, updated_student.tech_skills.all())
        self.assertIn(project_1, updated_student.projects.all())
        self.assertIn(project_2, updated_student.projects.all())

    def test_delete_one_item(self):
        self.authenticate()

        student_response = self.create_student(user=True)

        previous_db_counts = Student.objects.all().count()

        self.assertGreater(previous_db_counts, 0)
        self.assertEqual(previous_db_counts, 1)

        response = self.client.delete(reverse('student_detail', kwargs={'id': student_response.data['id']}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.all().count(), 0)

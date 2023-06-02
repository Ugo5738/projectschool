from accounts.models import User
from django.urls import reverse
from django.utils import timezone
from membership.models import Client, Instructor, Student
from project.models import Project, ProjectAttachment, Tag, Task, TechSkill
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ModelAPITestCase(APITestCase):
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
    
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin-test", email="admintest@test.com", password="admin", first_name='Admin', last_name='Admin', is_superuser=True)
        self.student_user = User.objects.create_user(username="stu-test", email="studenttest@test.com", password="student", first_name='Student', last_name='Student', is_student=True)
        self.instructor_user = User.objects.create_user(username="ins-test", email="instructortest@test.com", password="instructor", first_name='Instructor', last_name='Instructor', is_instructor=True)
        self.client_user = User.objects.create_user(username="client-test", email="clienttest@test.com", password="client", first_name='client', last_name='client', is_client=True)

        self.admin_user_2 = User.objects.create_user(username="admin-test_2", email="admintest2@test.com", password="admin2", first_name='Admin2', last_name='Admin2', is_superuser=True)
        self.student_user_2 = User.objects.create_user(username="stu-test_2", email="studenttest2@test.com", password="student2", first_name='Student2', last_name='Student2', is_student=True)
        self.instructor_user_2 = User.objects.create_user(username="ins-test_2", email="instructortest2@test.com", password="instructor2", first_name='Instructor2', last_name='Instructor2', is_instructor=True)
        self.client_user_2 = User.objects.create_user(username="client-test_2", email="clienttest2@test.com", password="client2", first_name='client2', last_name='client2', is_client=True)

        self.student = Student.objects.create(student=self.student_user, learning_style='visual')
        self.instructor = Instructor.objects.create(instructor=self.instructor_user, bio="Great Teacher!", experience=4, education="Google Certified", certifications="Python Advanced Certificate", rating=3.5, reviews=20000)
        self.clientele = Client.objects.create(client=self.client_user, company_name="Teckia", industry="Technology")

        # ALL THESE ARE FOR PROJECTS APP
        self.skill = TechSkill.objects.create(name='Python')
        self.skill_2 = TechSkill.objects.create(name='Django')
        self.tag = Tag.objects.create(name="Web Development")
        self.tag_2 = Tag.objects.create(name="Beginner")

        self.project_scope = ProjectAttachment.objects.create(name="Emotive Project Scope")
        self.ip_assignment = ProjectAttachment.objects.create(name="Emotive IP Assignment")
        self.project = Project.objects.create(title='Project 1', description='Project 1 Description', owner=self.admin_user, assigned_to=self.instructor_user, paid=False, budget=0.0)
        self.project.tags.add(self.tag)
        self.project.attachments.add(self.project_scope)
        self.project.attachments.add(self.ip_assignment)

        self.task_1 = Task.objects.create(project=self.project, title='Task 1', description='Task 1 Description', due_date=timezone.now(), estimated_hours=40, assigned_to=self.student_user, comments="Blog Phase 1")
        self.task_1.tags.add(self.tag_2)


class StudentAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'student': self.student_user_2.id,
            'goals': 'employment',
            'learning_style': 'visual',
            'availability': 'monday',
        }

    # TEST THE SEARCH FUNCTIONALITY

    def test_create_student_without_auth(self):
        url = reverse('student-list')
        
        initial_count = Student.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Student.objects.all().count(), initial_count)

    def test_create_student_with_auth(self):
        self.authenticate()

        initial_count = Student.objects.all().count()
        response = self.client.post(reverse('student-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.all().count(), initial_count + 1)

    def test_list_students_without_auth(self):
        url = reverse('student-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['learning_style'], self.student.learning_style)    

    def test_retrieve_student(self):
        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['learning_style'], self.student.learning_style)

    def test_update_student_with_auth(self):
        self.authenticate()

        url = reverse('student-detail', args=[self.student.pk])
        data = {'learning_style': 'auditory'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.learning_style, data['learning_style'])

    def test_delete_student_with_auth(self):
        self.authenticate()

        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0) 


class InstructorAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'instructor': self.instructor_user_2.id,
            'bio': 'Granular Teaching Tactics',
            'experience': 4,
            'education': 'Stanford University',
            'certifications': 'Google TensorFlow Certificate',
            'rating': 5.0,
        }

    # TEST THE SEARCH FUNCTIONALITY

    def test_create_instructor_without_auth(self):
        url = reverse('instructor-list')
        
        initial_count = Instructor.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Instructor.objects.all().count(), initial_count)

    def test_create_instructor_with_auth(self):
        self.authenticate()

        initial_count = Instructor.objects.all().count()
        response = self.client.post(reverse('instructor-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Instructor.objects.all().count(), initial_count + 1)

    def test_list_instructors_without_auth(self):
        url = reverse('instructor-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_instructors_with_auth(self):
        self.authenticate()

        url = reverse('instructor-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['education'], self.instructor.education)

    def test_retrieve_instructor_without_auth(self):
        url = reverse('instructor-detail', args=[self.instructor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_instructor_with_auth(self):
        self.authenticate()

        url = reverse('instructor-detail', args=[self.instructor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['education'], self.instructor.education)

    def test_update_instructor_with_auth(self):
        self.authenticate()

        url = reverse('instructor-detail', args=[self.instructor.pk])
        data = {'education': 'MIT'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.instructor.refresh_from_db()
        self.assertEqual(self.instructor.education, data['education'])

    def test_delete_instructor_with_auth(self):
        self.authenticate()

        url = reverse('instructor-detail', args=[self.instructor.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Instructor.objects.count(), 0) 


class ClientAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'client': self.client_user_2.id,
            'company_name': 'Teckinia',
            'industry': 'Ecommerce',
        }

    # TEST THE SEARCH FUNCTIONALITY

    def test_create_client_without_auth(self):
        url = reverse('client-list')
        
        initial_count = Client.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.all().count(), initial_count)

    def test_create_client_with_auth(self):
        self.authenticate()

        initial_count = Client.objects.all().count()
        response = self.client.post(reverse('client-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), initial_count + 1)

    def test_list_clients_without_auth(self):
        url = reverse('client-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_clients_with_auth(self):
        self.authenticate()

        url = reverse('client-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['company_name'], self.clientele.company_name)

    def test_retrieve_client_without_auth(self):
        url = reverse('client-detail', args=[self.clientele.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_client_with_auth(self):
        self.authenticate()

        url = reverse('client-detail', args=[self.clientele.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], self.clientele.company_name)

    def test_update_client_with_auth(self):
        self.authenticate()

        url = reverse('client-detail', args=[self.clientele.pk])
        data = {'company_name': 'Teknon'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.clientele.refresh_from_db()
        self.assertEqual(self.clientele.company_name, data['company_name'])

    def test_delete_client_with_auth(self):
        self.authenticate()

        url = reverse('client-detail', args=[self.clientele.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0) 

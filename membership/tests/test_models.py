from accounts.models import User
from django.utils import timezone
from membership.models import Client, Instructor, Student
from project.models import Project, ProjectAttachment, Tag, Task, TechSkill
from rest_framework.test import APITestCase


class APITestCaseSetUp(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin-test",
            email="admintest@test.com",
            password="admin",
            first_name='Admin',
            last_name='Admin',
            is_superuser=True
        )
        self.student_user = User.objects.create_user(
            username="stu-test",
            email="studenttest@test.com",
            password="student",
            first_name='Student',
            last_name='Student',
            is_student=True
        )
        self.instructor_user = User.objects.create_user(
            username="ins-test",
            email="instructortest@test.com",
            password="instructor",
            first_name='Instructor',
            last_name='Instructor',
            is_instructor=True
        )
        self.client_user = User.objects.create_user(
            username="client-test",
            email="clienttest@test.com",
            password="client",
            first_name='Client',
            last_name='Client',
            is_client=True
        )
        self.student = Student.objects.create(
            student=self.student_user,
            learning_style='visual'
        )
        self.instructor = Instructor.objects.create(
            instructor=self.instructor_user,
            bio="Great Teacher!",
            experience=4,
            education="Google Certified",
            certifications="Python Advanced Certificate",
            rating=3.5,
            reviews=20000
        )
        self.client = Client.objects.create(
            client=self.client_user,
            company_name="Test Company",
            industry="Technology"
        )

        self.skill = TechSkill.objects.create(name='Python')
        self.tag = Tag.objects.create(name="Web Development")
        self.project = Project.objects.create(
            title='Project 1',
            description='Project 1 Description',
            owner=self.admin_user,
            assigned_to=self.instructor_user,
            paid=False,
            budget=0.0
        )
        self.project.tags.add(self.tag)
        self.project_attachment = ProjectAttachment.objects.create(name="Test Attachment")
        self.project.attachments.add(self.project_attachment)
        self.task = Task.objects.create(
            project=self.project,
            title='Task 1',
            description='Task 1 Description',
            due_date=timezone.now(),
            assigned_to=self.student_user
        )

class StudentModelTestCase(APITestCaseSetUp):
    def test_student_model(self):
        self.assertEqual(str(self.student), str(self.student_user.get_full_name))
        self.assertEqual(self.student.learning_style, 'visual')
        self.assertTrue(isinstance(self.student, Student))
        self.assertTrue(isinstance(self.student.student, User))


class InstructorModelTestCase(APITestCaseSetUp):
    def test_instructor_model(self):
        self.assertEqual(str(self.instructor), str(self.instructor_user.get_full_name))
        self.assertEqual(self.instructor.bio, 'Great Teacher!')
        self.assertEqual(self.instructor.experience, 4)
        self.assertEqual(self.instructor.education, 'Google Certified')
        self.assertEqual(self.instructor.certifications, 'Python Advanced Certificate')
        self.assertEqual(self.instructor.rating, 3.5)
        self.assertEqual(self.instructor.reviews, 20000)
        self.assertTrue(isinstance(self.instructor, Instructor))
        self.assertTrue(isinstance(self.instructor.instructor, User))


class ClientModelTestCase(APITestCaseSetUp):
    def test_client_model(self):
        self.assertEqual(str(self.client_user.get_full_name), 'Client Client')
        self.assertTrue(self.client_user.is_client)
        self.assertTrue(isinstance(self.client_user, User))


class SearchTestCase(APITestCaseSetUp):
    def test_search_students(self):
        student_results, instructor_results, client_results = Student.objects.search(query='visual')
        self.assertEqual(len(student_results), 1)  

        student_results, instructor_results, client_results = Student.objects.search(query='goals')
        self.assertEqual(len(student_results), 0)  

    def test_search_instructors(self):
        student_results, instructor_results, client_results = Instructor.objects.search(query='bio')
        self.assertEqual(len(instructor_results), 0)  

        student_results, instructor_results, client_results = Instructor.objects.search(query='education')
        self.assertEqual(len(instructor_results), 0)  

    def test_search_clients(self):
        student_results, instructor_results, client_results = Client.objects.search(query='company')
        self.assertEqual(len(client_results), 1)  

        student_results, instructor_results, client_results = Client.objects.search(query='industry')
        self.assertEqual(len(client_results), 0)  
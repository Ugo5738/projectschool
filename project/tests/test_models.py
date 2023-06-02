from accounts.models import User
from django.test import TestCase
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
        self.clientele = Client.objects.create(
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
        self.task.tags.add(self.tag)


class TechSkillModelTestCase(APITestCaseSetUp):
    def test_tech_skill_model(self):
        self.assertEqual(str(self.skill), 'Python')
        self.assertTrue(isinstance(self.skill, TechSkill))


class ProjectModelTestCase(APITestCaseSetUp):
    def test_project_model(self):
        self.assertEqual(self.project.title, 'Project 1')
        self.assertEqual(self.project.description, 'Project 1 Description')
        self.assertEqual(self.project.owner, self.admin_user)
        self.assertEqual(self.project.assigned_to, self.instructor_user)
        self.assertFalse(self.project.paid)
        self.assertEqual(self.project.budget, 0.0)
        self.assertEqual(self.project.tags.count(), 1)
        self.assertTrue(isinstance(self.project, Project))


class TaskModelTestCase(APITestCaseSetUp):
    def test_task_model(self):
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.title, 'Task 1')
        self.assertEqual(self.task.description, 'Task 1 Description')
        self.assertEqual(self.task.due_date.date(), timezone.now().date())
        self.assertEqual(self.task.assigned_to, self.student_user)
        self.assertEqual(self.task.tags.count(), 1)
        self.assertTrue(isinstance(self.task, Task))


class ProjectAttachmentModelTestCase(APITestCaseSetUp):
    def test_project_attachment_model(self):
        self.assertEqual(self.project_attachment.name, "Test Attachment")
        self.assertTrue(isinstance(self.project_attachment, ProjectAttachment))


class TagModelTestCase(APITestCaseSetUp):
    def test_tag_model(self):
        self.assertEqual(self.tag.name, "Web Development")
        self.assertTrue(isinstance(self.tag, Tag))

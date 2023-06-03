from datetime import date

from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from membership.models import Client, Instructor, Student
from project.models import (Activity, Project, ProjectAttachment, Tag, Task,
                            TechSkill)
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

        self.file_1 = ProjectAttachment.objects.create(name="Emotive Project Scope")
        self.file_2 = ProjectAttachment.objects.create(name="Emotive IP Assignment")
        self.project = Project.objects.create(title='Project 1', description='Project 1 Description', owner=self.admin_user, assigned_to=self.instructor_user, paid=False, budget=0.0)
        self.project.tags.add(self.tag)
        self.project.attachments.add(self.file_1)
        self.project.attachments.add(self.file_2)

        self.task_1 = Task.objects.create(project=self.project, title='Task 1', description='Task 1 Description', due_date=timezone.now(), estimated_hours=40, assigned_to=self.student_user, comments="Blog Phase 1")
        self.task_1.tags.add(self.tag_2)

        self.activity = Activity.objects.create(user=self.admin_user, project=self.project, task=self.task_1, activity_type='updated_task')


class TechSkillAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'name': 'JavaScript',
        }

    def test_create_tech_skills_without_auth(self):
        url = reverse('tech_skill-list')
        
        initial_count = TechSkill.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(TechSkill.objects.all().count(), initial_count)

    def test_create_tech_skills_with_auth(self):
        self.authenticate()

        initial_count = TechSkill.objects.all().count()
        response = self.client.post(reverse('tech_skill-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TechSkill.objects.all().count(), initial_count + 1)

    def test_list_tech_skills_without_auth(self):
        url = reverse('tech_skill-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['name'], self.skill.name)

    def test_retrieve_tech_skill(self):
        url = reverse('tech_skill-detail', args=[self.skill.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.skill.name)

    def test_update_tech_skill_with_auth(self):
        self.authenticate()

        url = reverse('tech_skill-detail', args=[self.skill.pk])
        data = {'name': 'Blockchain'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, data['name'])

    def test_delete_tech_skill_with_auth(self):
        self.authenticate()

        url = reverse('tech_skill-detail', args=[self.skill.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TechSkill.objects.count(), 1) 


class ProjectAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'title': 'Project 22',
            'description': 'Project 22 Description',
            'owner': self.client_user.id,
            'assigned_to': self.instructor_user.id,
            'paid': True,
            'budget': 100000.0,
        }

    def test_create_project_without_auth(self):
        url = reverse('project-list')
        
        initial_count = Project.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Project.objects.all().count(), initial_count)

    def test_create_project_with_auth(self):
        self.authenticate()

        initial_count = Project.objects.all().count()
        response = self.client.post(reverse('project-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.all().count(), initial_count + 1)

    def test_list_projects_without_auth(self):
        url = reverse('project-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.project.title)

    def test_retrieve_project(self):
        url = reverse('project-detail', args=[self.project.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)

    def test_update_project_without_auth(self):
        url = reverse('project-detail', args=[self.project.pk])
        data = {'title': 'Project 24'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project_with_auth(self):
        self.authenticate()

        url = reverse('project-detail', args=[self.project.pk])
        data = {'title': 'Project 24'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, data['title'])

    def test_delete_project_with_auth(self):
        self.authenticate()

        url = reverse('project-detail', args=[self.project.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0) 


class TaskAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'project': self.project.pk,
            'title': 'Task 2',
            'description': 'Task 2 Description',
            'due_date': str(date.today()),
            'estimated_hours': 20,
            'assigned_to': self.student_user.id,
            'comments': 'New task',
        }

    def test_create_task_without_auth(self):
        url = reverse('task-list')
        
        initial_count = Task.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.all().count(), initial_count)

    def test_create_task_with_auth(self):
        self.authenticate()

        initial_count = Task.objects.all().count()
        response = self.client.post(reverse('task-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), initial_count + 1)

    def test_list_tasks_without_auth(self):
        url = reverse('task-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_without_auth(self):
        url = reverse('task-detail', args=[self.task_1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_task_with_auth(self):
        self.authenticate()

        url = reverse('task-detail', args=[self.task_1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_1.title)

    def test_update_task_without_auth(self):
        url = reverse('task-detail', args=[self.task_1.pk])
        data = {'title': 'Updated Task 1'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_with_auth(self):
        self.authenticate()

        url = reverse('task-detail', args=[self.task_1.pk])
        data = {'title': 'Updated Task 1'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_1.refresh_from_db()
        self.assertEqual(self.task_1.title, data['title'])

    def test_delete_task_without_auth(self):
        url = reverse('task-detail', args=[self.task_1.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_task_with_auth(self):
        self.authenticate()

        url = reverse('task-detail', args=[self.task_1.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class ProjectAttachmentAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        text_file = SimpleUploadedFile(
            name='project_file.pdf',
            content=b'file_content',
            content_type='application/pdf'
        )

        self.data = {
            'name': 'Project File 3',
            'file': text_file,
            'comments': 'Additional comments',
        }

        self.project.attachments.add(self.file_1)
        self.project.attachments.add(self.file_2)

    def test_create_project_attachment_without_auth(self):
        url = reverse('projectattachment-list')

        response = self.client.post(url, self.data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_attachment_with_auth(self):
        self.authenticate()

        initial_count = ProjectAttachment.objects.all().count()
        response = self.client.post(reverse('projectattachment-list'), self.data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectAttachment.objects.all().count(), initial_count + 1)

    def test_list_project_attachments_without_auth(self):
        url = reverse('projectattachment-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_project_attachments_with_auth(self):
        self.authenticate()

        num_attachments = ProjectAttachment.objects.all().count()

        url = reverse('projectattachment-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), num_attachments)

    def test_retrieve_project_attachment_without_auth(self):
        url = reverse('projectattachment-detail', args=[self.file_1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_project_attachment_with_auth(self):
        self.authenticate()

        url = reverse('projectattachment-detail', args=[self.file_1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.file_1.name)

    def test_update_project_attachment_without_auth(self):
        url = reverse('projectattachment-detail', args=[self.file_1.pk])
        data = {'name': 'Updated Project File 1'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project_attachment_with_auth(self):
        self.authenticate()

        url = reverse('projectattachment-detail', args=[self.file_1.pk])
        data = {'name': 'Updated Project File 1'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.file_1.refresh_from_db()
        self.assertEqual(self.file_1.name, data['name'])

    def test_delete_project_attachment_without_auth(self):
        url = reverse('projectattachment-detail', args=[self.file_1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(ProjectAttachment.objects.filter(pk=self.file_1.pk).exists())

    def test_delete_project_attachment_with_auth(self):
        self.authenticate()
        url = reverse('projectattachment-detail', args=[self.file_1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProjectAttachment.objects.filter(id=self.file_1.id).exists())

    # def test_project_attachment_pagination(self):
    #     from math import ceil

    #     from project.views import ProjectAttachmentCustomPageNumberPagination
        
    #     self.authenticate()

    #     # Create test data

    #     # Make the request to the API
    #     url = reverse('projectattachment-list')
    #     response = self.client.get(url)

    #     # Check the response status code
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Check the pagination details
    #     response_data = response.data
    #     self.assertIn('results', response_data)
    #     self.assertIn('count', response_data)
    #     self.assertIn('next', response_data)
    #     self.assertIn('previous', response_data)

    #     # Get the number of project attachments from the response
    #     project_attachments_count = response_data['count']

    #     # Calculate the expected number of pages based on the page size
    #     expected_num_pages = (project_attachments_count + 9) // 10  # Ceiling division

    #     # Check the number of project attachments in the response
    #     self.assertEqual(len(response_data['results']), min(project_attachments_count, 10))

    #     expected_project_attachments_count = ProjectAttachment.objects.count()

    #     # Get the expected URL for the next page
    #     page_number = 2
    #     next_url = f'http://testserver{url}?page={page_number}'
    #     if response_data['next'] is None:
    #         expected_next_url = None
    #     else:
    #         expected_next_url = next_url

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_data['count'], expected_project_attachments_count)
    #     self.assertEqual(response_data['next'], expected_next_url)
    #     self.assertEqual(response_data['previous'], None)
    #     self.assertEqual(len(response_data['results']), expected_project_attachments_count)

    #     # Retrieve the next page results
    #     next_url = response_data['next']
    #     if next_url:
    #         next_response = self.client.get(next_url)

    #         # Check the response status code
    #         self.assertEqual(next_response.status_code, status.HTTP_200_OK)

    #         # Check the pagination details of the second page
    #         next_response_data = next_response.data
    #         self.assertIn('results', next_response_data)
    #         self.assertIn('count', next_response_data)
    #         self.assertIn('next', next_response_data)
    #         self.assertIn('previous', next_response_data)

    #         # Check the number of project attachments in the second page
    #         self.assertEqual(len(next_response_data['results']), min(project_attachments_count - 10, 10))


class TagAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'name': 'Advanced',
        }

    def test_create_tags_without_auth(self):
        initial_count = Tag.objects.all().count()
        
        url = reverse('tag-list')
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Tag.objects.all().count(), initial_count)

    def test_create_tags_with_auth(self):
        self.authenticate()

        initial_count = Tag.objects.all().count()

        response = self.client.post(reverse('tag-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.all().count(), initial_count)

    def test_list_tags_without_auth(self):
        num_tags = Tag.objects.all().count()

        url = reverse('tag-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), num_tags)
        self.assertEqual(response_data_dict[0]['name'], self.tag.name)

    def test_retrieve_tag(self):
        url = reverse('tag-detail', args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tag.name)

    def test_update_tag_with_auth(self):
        self.authenticate()

        url = reverse('tag-detail', args=[self.tag.pk])
        data = {'name': 'Blockchain'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, data['name'])

    def test_delete_tag_with_auth(self):
        self.authenticate()

        url = reverse('tag-detail', args=[self.tag.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 1) 


class ActivityAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'user': self.admin_user.id,
            'project': self.project.id,
            'task': self.task_1.id,
            'activity_type': 'created_task',
        }

    def test_create_activity_without_auth(self):
        url = reverse('activity-list')
        
        initial_count = Activity.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Activity.objects.all().count(), initial_count)

    def test_create_activity_with_auth(self):
        self.authenticate()

        initial_count = Activity.objects.all().count()
        response = self.client.post(reverse('activity-list'), self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.all().count(), initial_count + 1)

    def test_list_activities_without_auth(self):
        url = reverse('activity-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['activity_type'], self.data['activity_type'])

    def test_retrieve_activity(self):
        url = reverse('activity-detail', args=[self.activity.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], self.activity.activity_type)

    def test_update_activity_with_auth(self):
        self.authenticate()

        url = reverse('activity-detail', args=[self.activity.pk])
        data = {'activity_type': 'updated_task'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.activity_type, data['activity_type'])

    def test_delete_activity_with_auth(self):
        self.authenticate()
        num_activity = Activity.objects.all().count()

        url = reverse('activity-detail', args=[self.activity.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activity.objects.count(), num_activity - 1)
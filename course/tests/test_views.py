import datetime

from accounts.models import User
from course.models import (Answer, Course, CourseContent, CourseDetails,
                           CourseMetadata, Enrollment, File, Lesson, Module,
                           Program, Question, Quiz, Video)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from membership.models import Instructor, Student
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

    def create_instructor(self, user=False):
        sample_instructor = {
                'bio': 'Great Teacher!', 
                'experience': 4,
                'education': 'Google Developer Certified',
                'certifications': 'Python Advanced Certificate',
                'rating': 3.5,
                'reviews': 20000,
            }

        if user:
            user = User.objects.get(email="test@test.com")
            sample_instructor['instructor'] = user.id

        response = self.client.post(reverse('instructor'), sample_instructor)
        
        return response
    
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin-test", email="admintest@test.com", password="admin", first_name='Admin', last_name='Admin', is_superuser=True)
        self.student_user = User.objects.create_user(username="stu-test", email="studenttest@test.com", password="student", first_name='Student', last_name='Student', is_student=True)
        self.instructor_user = User.objects.create_user(username="ins-test", email="instructortest@test.com", password="instructor", first_name='Instructor', last_name='Instructor', is_instructor=True)
        self.client_user = User.objects.create_user(username="client-test", email="clienttest@test.com", password="client", first_name='client', last_name='client', is_client=True)

        self.student = Student.objects.create(student=self.student_user, learning_style='visual')
        self.instructor = Instructor.objects.create(instructor=self.instructor_user, bio="Great Teacher!", experience=4, education="Google Certified", certifications="Python Advanced Certificate", rating=3.5, reviews=20000)

        self.program = Program.objects.create(title='Test Program', description='Test Program Description', price=19.99, duration=10)
        self.program_2 = Program.objects.create(title='Test Program 2', description='Test Program Description 2', price=99.99, duration=12)
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

        self.metadata = CourseMetadata.objects.create(level='beginner', rating=4.5, price=9.99, certificate=True)
        self.content = CourseContent.objects.create(syllabus='Course Syllabus', prerequisites='Have a basic understanding of coding.')
        self.details = CourseDetails.objects.create(instructor=self.instructor, program=self.program, projects=self.project)
        self.details.skills.add(self.skill)
        self.details.skills.add(self.skill_2)

        self.metadata_2 = CourseMetadata.objects.create(level='Intermediate', rating=4.5, price=99.99, certificate=True)
        self.content_2 = CourseContent.objects.create(syllabus='Course Syllabus', prerequisites='Have an intermediate understanding of coding.')
        self.details_2 = CourseDetails.objects.create(instructor=self.instructor, program=self.program, projects=self.project)
        self.details_2.skills.add(self.skill)

        self.metadata_3 = CourseMetadata.objects.create(level='Advanced', rating=5.0, price=99.99, certificate=True)
        self.content_3 = CourseContent.objects.create(syllabus='Course Syllabus', prerequisites='Have an Advanced understanding of coding.')
        self.details_3 = CourseDetails.objects.create(instructor=self.instructor, program=self.program, projects=self.project)
        self.details_3.skills.add(self.skill_2)

        self.course = Course.objects.create(title='Test Course', description='Test Course Description', metadata=self.metadata, content=self.content, details=self.details)
        self.course_2 = Course.objects.create(title='Test Course 2', description='Test Course Description 2', metadata=self.metadata_2, content=self.content_2, details=self.details_2)
        self.course_3 = Course.objects.create(title='Test Course 3', description='Test Course Description 3', metadata=self.metadata_3, content=self.content_3, details=self.details_3)

        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Quiz Description', total_marks=10)
        self.question = Question.objects.create(quiz=self.quiz, text='Test Question', marks=2)
        self.answer = Answer.objects.create(question=self.question, text='Test Answer', is_correct=True)
        self.module = Module.objects.create(title='Test Module', description='Week 1 module', course=self.course, order=1, duration=4, quiz=self.quiz)
        self.lesson = Lesson.objects.create(module=self.module, title="First Lesson", content="First lesson Content", order=1, duration=15)
        self.video = Video.objects.create(title='Test Video', lesson=self.lesson, video_file='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.file = File.objects.create(title='Test File', description='This is a test file', lesson=self.lesson, file='file.pdf')
        
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course, program=self.program)



class ProgramAPITestCase(ModelAPITestCase):
    def get_data(self):
        # super().setUp()
        self.data = {
            'title': 'New Test Program',
            'description': 'This is a new test program.',
            'price': 19.99, 
            'duration': 10
        }
    
    def test_create_program_without_auth(self):
        self.get_data()
        
        url = reverse('program-list')        

        initial_count = Program.objects.all().count()
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Program.objects.all().count(), initial_count)

    def test_create_program_with_auth(self):
        self.get_data()
        self.authenticate()
        
        url = reverse('program-list')
        
        initial_count = Program.objects.all().count()
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Program.objects.all().count(), initial_count+1)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_list_programs_without_auth(self):
        url = reverse('program-list')
        
        response = self.client.get(url)
        response_data_dict = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.program.title)

    def test_retrieve_program(self):
        url = reverse('program-detail', args=[self.program.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.program.title)

    def test_update_program_with_auth(self):
        self.authenticate()

        url = reverse('program-detail', args=[self.program.pk])
        data = {'title': 'Updated Test Program'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.program.refresh_from_db()
        self.assertEqual(self.program.title, data['title'])

    def test_update_program_without_auth(self):
        url = reverse('program-detail', args=[self.program.pk])
        data = {'title': 'Updated Test Program'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.program.refresh_from_db()
        
    def test_delete_program(self):
        self.authenticate()

        url = reverse('program-detail', args=[self.program.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Program.objects.count(), 0)



class CourseAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'title': 'Test Course',
            'description': 'Test Course Description',
            'metadata': {
                'level': 'beginner',
                'rating': 4.5,
                'price': 9.99,
                'certificate': True
            },
            'content': {
                'syllabus': 'Course Syllabus',
                'prerequisites': 'Have a basic understanding of coding.'
            },
            'details': {
                'instructor': self.instructor.id,
                'program': self.program.id,
                'projects': self.project.id,
                'skills': [self.skill.id, self.skill_2.id]
            },
        }

        # self.data = {
        #     'title': 'New Test Course',
        #     'description': 'This is a new test course.',
        #     'metadata': self.metadata,
        #     'content': self.content,
        #     'details': self.details,
        # }  # requires changing the serializers
    
    def test_create_course_without_auth(self):
        # self.get_data()
        url = reverse('course-list')
        
        initial_count = Course.objects.all().count()
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Course.objects.all().count(), initial_count)

    def test_create_course_with_auth(self):
        self.authenticate()

        response = self.client.post(reverse('course-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_courses_without_auth(self):
        url = reverse('course-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.course.title)    

    def test_retrieve_course(self):
        url = reverse('course-detail', args=[self.course.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

    def test_update_course_with_auth(self):
        self.authenticate()

        url = reverse('course-detail', args=[self.course.pk])
        data = {'title': 'Updated Test Course'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, data['title'])

    def test_delete_course_with_auth(self):
        self.authenticate()

        url = reverse('course-detail', args=[self.course.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0) 



class QuizAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'title': 'New Quiz',
            'description': 'New Quiz Description',
            'total_marks': 20
        }

    def test_create_quiz_without_auth(self):
        url = reverse('quiz-list')

        initial_count = Quiz.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Quiz.objects.all().count(), initial_count)

    def test_create_quiz_with_auth(self):
        self.authenticate()
        url = reverse('quiz-list')

        initial_count = Quiz.objects.all().count()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.all().count(), initial_count + 1)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_list_quizzes_without_auth(self):
        url = reverse('quiz-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_quizzes_with_auth(self):
        self.authenticate()

        url = reverse('quiz-list')
        response = self.client.get(url)
        print(response.data)
        response_data_dict = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.quiz.title)

    def test_retrieve_quiz_without_auth(self):
        url = reverse('quiz-detail', args=[self.quiz.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_quiz_without_auth(self):
        url = reverse('quiz-detail', args=[self.quiz.pk])
        data = {'title': 'Updated Quiz'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.quiz.refresh_from_db()
        self.assertNotEqual(self.quiz.title, data['title'])

    def test_update_quiz_with_auth(self):
        self.authenticate()
        url = reverse('quiz-detail', args=[self.quiz.pk])
        data = {'title': 'Updated Quiz'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, data['title'])

    def test_delete_quiz_without_auth(self):
        url = reverse('quiz-detail', args=[self.quiz.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_delete_quiz_with_auth(self):
        self.authenticate()
        url = reverse('quiz-detail', args=[self.quiz.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)



class AnswerAPITestCase(ModelAPITestCase):
    def test_list_answers_without_auth(self):
        url = reverse('answer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_answers_with_auth(self):
        self.authenticate()
        url = reverse('answer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_answer_without_auth(self):
        url = reverse('answer-list')
        data = {'question': self.question.id, 'text': 'Test Answer', 'is_correct': False}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_answer_with_auth(self):
        self.authenticate()
        url = reverse('answer-list')
        data = {'question': self.question.id, 'text': 'Test Answer', 'is_correct': False}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_answer_without_auth(self):
        url = reverse('answer-detail', args=[self.answer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_answer_with_auth(self):
        self.authenticate()
        url = reverse('answer-detail', args=[self.answer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_answer_without_auth(self):
        url = reverse('answer-detail', args=[self.answer.id])
        data = {'text': 'Updated Answer'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_answer_with_auth(self):
        self.authenticate()
        url = reverse('answer-detail', args=[self.answer.id])
        data = {'text': 'Updated Answer'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer_without_auth(self):
        url = reverse('answer-detail', args=[self.answer.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_answer_with_auth(self):
        self.authenticate()
        url = reverse('answer-detail', args=[self.answer.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class QuestionAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'quiz': self.quiz.id,
            'text': 'What is the capital of France?',
            'marks': 10,
            'correct_answer': 'Paris',
        }

    def test_list_questions_without_auth(self):
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_questions_with_auth(self):
        self.authenticate()
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question_without_auth(self):
        url = reverse('question-list')
        
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_question_with_auth(self):
        self.authenticate()
        url = reverse('question-list')
        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
        
        question = Question.objects.latest('id')
        self.assertEqual(question.text, 'What is the capital of France?')
        self.assertEqual(question.correct_answer, 'Paris')
        self.assertEqual(question.marks, 10)
        self.assertEqual(question.quiz, self.quiz)

    def test_retrieve_question_without_auth(self):
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_question_with_auth(self):
        self.authenticate()
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_without_auth(self):
        url = reverse('question-detail', args=[self.question.id])
        data = {
            'quiz': self.quiz.id,
            'text': 'Updated Question',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.question.refresh_from_db()
        self.assertNotEqual(self.question.text, data['text']) 
    
    def test_update_question_with_auth(self):
        self.authenticate()
        url = reverse('question-detail', args=[self.question.id])
        data = {
            'quiz': self.quiz.id,
            'text': 'Updated Question',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, data['text'])

    def test_delete_question_with_auth(self):
        self.authenticate()
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())



class ModuleAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'title': 'Test Module',
            'description': 'Module Description',
            'course': self.course.id,
            'order': 1,
            'duration': 4,
            'is_published': True,
            'quiz': self.quiz.id
        }


    def test_create_module_without_auth(self):
        url = reverse('module-list')
        
        initial_count = Module.objects.all().count()
        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Module.objects.all().count(), initial_count)


    def test_create_module_with_auth(self):
        self.authenticate()
        url = reverse('module-list')
        
        initial_count = Module.objects.all().count()
        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.all().count(), initial_count + 1)
        self.assertEqual(response.data['title'], self.data['title'])


    def test_list_modules_without_auth(self):
        url = reverse('module-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.module.title)


    def test_retrieve_module(self):
        url = reverse('module-detail', args=[self.module.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.module.title)


    def test_update_module_with_auth(self):
        self.authenticate()

        url = reverse('module-detail', args=[self.module.pk])
        data = {'title': 'Updated Test Module'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, data['title'])


    def test_update_module_without_auth(self):
        url = reverse('module-detail', args=[self.module.pk])
        data = {'title': 'Updated Test Module'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.module.refresh_from_db()


    def test_delete_module_with_auth(self):
        self.authenticate()
        url = reverse('module-detail', args=[self.module.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.count(), 0)



class LessonAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        self.data = {
            'module': self.module.id,
            'title': 'Lesson Description',
            'content': 'Lesson content',
            'order': 1,
            'duration': 4,
            'is_published': True,
        }


    def test_list_lessons_without_auth(self):
        url = reverse('lesson-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.lesson.title)


    def test_create_lesson_without_auth(self):
        url = reverse('lesson-list')
        
        initial_count = Lesson.objects.all().count()
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.all().count(), initial_count)


    def test_create_lesson_with_auth(self):
        self.authenticate()

        url = reverse('lesson-list')
        initial_count = Lesson.objects.all().count()
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), initial_count + 1)
        self.assertEqual(response.data['title'], self.data['title'])


    def test_retrieve_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)
    

    def test_update_lesson_without_auth(self):
        data = {'title': 'Updated Lesson'}

        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_lesson_with_auth(self):
        self.authenticate()

        data = {'title': 'Updated Lesson'}

        url = reverse('lesson-detail', args=[self.lesson.pk])
        
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data['title'])


    def test_delete_lesson_without_auth(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    def test_delete_lesson_with_auth(self):
        self.authenticate()

        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 
        self.assertEqual(Lesson.objects.count(), 0)



class VideoAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        video_file = SimpleUploadedFile(
            name='sample_video.mp4',
            content=b'video_content',
            content_type='video/mp4'
        )

        self.data = {
            'title': 'New Video',
            'lesson': self.lesson.id,
            'description': 'This is a tutorial',
            'video_file': video_file,
        }

    def test_create_video_without_auth(self):
        url = reverse('video-list')
        response = self.client.post(url, self.data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Video.objects.all().count(), 1)

    def test_create_video_with_auth(self):
        self.authenticate()
        url = reverse('video-list')
        response = self.client.post(url, self.data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.all().count(), 2)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_list_videos_without_auth(self):
        url = reverse('video-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_videos_with_auth(self):
        self.authenticate()
        url = reverse('video-list')
        response = self.client.get(url)
        response_data_dict = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_dict), 1)
        self.assertEqual(response_data_dict[0]['title'], self.video.title)

    def test_retrieve_video_without_auth(self):
        url = reverse('video-detail', args=[self.video.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_video_with_auth(self):
        self.authenticate()
        url = reverse('video-detail', args=[self.video.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.video.title)

    def test_update_video_without_auth(self):
        url = reverse('video-detail', args=[self.video.pk])
        data = {'title': 'Updated Video'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.video.refresh_from_db()
        self.assertNotEqual(self.video.title, data['title'])

    def test_update_video_with_auth(self):
        self.authenticate()
        url = reverse('video-detail', args=[self.video.pk])
        data = {'title': 'Updated Video'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, data['title'])

    def test_delete_video_without_auth(self):
        url = reverse('video-detail', args=[self.video.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Video.objects.count(), 1)

    def test_delete_video_with_auth(self):
        self.authenticate()
        url = reverse('video-detail', args=[self.video.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Video.objects.count(), 0)



class FileAPITestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()
        
        text_file = SimpleUploadedFile(
            name='sample_text.pdf',
            content=b'text_content',
            content_type='application/pdf'
        )

        self.data = {
            'title': 'New File',
            'lesson': self.lesson.id,
            'description': 'This is a tutorial file',
            'file': text_file,
        }

    def test_create_file_without_auth(self):
        url = reverse('file-list')
        
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_file_with_auth(self):
        self.authenticate()

        url = reverse('file-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 2)

        file = File.objects.latest('id')
        self.assertEqual(file.title, 'New File')
        self.assertEqual(file.description, 'This is a tutorial file')
        self.assertEqual(file.lesson, self.lesson)

    def test_list_files_without_auth(self):
        url = reverse('file-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(File.objects.all().count(), 1)

    def test_list_files_with_auth(self):
        self.authenticate()
        url = reverse('file-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_file_without_auth(self):
        url = reverse('file-detail', args=[self.file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_file_with_auth(self):
        self.authenticate()
        url = reverse('file-detail', args=[self.file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_file_without_auth(self):
        url = reverse('file-detail', args=[self.file.id])
        data = {'title': 'Updated File'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.file.refresh_from_db()
        self.assertNotEqual(self.file.title, data['title'])

    def test_update_file_with_auth(self):
        self.authenticate()
        url = reverse('file-detail', args=[self.file.id])
        data = {'title': 'Updated File'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.file.refresh_from_db()
        self.assertEqual(self.file.title, data['title'])

    def test_delete_file_without_auth(self):
        url = reverse('file-detail', args=[self.file.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(File.objects.filter(id=self.file.id).exists())

    def test_delete_file_with_auth(self):
        self.authenticate()
        url = reverse('file-detail', args=[self.file.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(File.objects.filter(id=self.file.id).exists())



class EnrollmentTestCase(ModelAPITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            'student': self.student.id,
            'course': self.course_2.id,
            'program': self.program.id
        }

    def test_create_enrollment_without_auth(self):
        url = reverse('enrollment-list')
        
        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_enrollment_with_auth(self):
        self.authenticate()
        url = reverse('enrollment-list')
        
        response = self.client.post(url, self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 2)
        self.assertEqual(Enrollment.objects.first().student, self.student)
        self.assertEqual(Enrollment.objects.first().course, self.course)
        self.assertEqual(Enrollment.objects.first().program, self.program)

    def test_retrieve_enrollment_without_auth(self):
        url = reverse('enrollment-detail', kwargs={'pk': self.enrollment.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['id'], self.enrollment.id)
        self.assertEqual(response.data['student'], self.student.id)
        self.assertEqual(response.data['course'], self.course.id)
        self.assertEqual(response.data['program'], self.program.id)

    def test_retrieve_enrollment_without_auth(self):
        self.authenticate()
        url = reverse('enrollment-detail', kwargs={'pk': self.enrollment.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.enrollment.id)
        self.assertEqual(response.data['student'], self.student.id)
        self.assertEqual(response.data['course'], self.course.id)
        self.assertEqual(response.data['program'], self.program.id)

    def test_update_enrollment(self):
        self.authenticate()

        url = reverse('enrollment-detail', kwargs={'pk': self.enrollment.id})

        updated_data = {
            'student': self.student.id,
            'course': self.course_3.id,
            'program': self.program.id
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.enrollment.id)
        self.assertEqual(response.data['student'], self.student.id)
        self.assertEqual(response.data['course'], self.course_3.id)
        self.assertEqual(response.data['program'], self.program.id)

    def test_delete_enrollment(self):
        self.authenticate()

        url = reverse('enrollment-detail', kwargs={'pk': self.enrollment.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 0)
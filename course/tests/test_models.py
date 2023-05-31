from accounts.models import User
from course.models import (Answer, Course, CourseContent, CourseDetails,
                           CourseMetadata, Enrollment, File, Lesson, Module,
                           Program, Question, Quiz, Video)
from django.db import IntegrityError
from django.utils import timezone
from membership.models import Instructor, Student
from project.models import Project, ProjectAttachment, Tag, Task, TechSkill
from rest_framework.test import APITestCase


class APITestCaseSetUp(APITestCase):
    def set_up(self):
        self.admin_user = User.objects.create_user(username="admin-test", email="admintest@test.com", password="admin", first_name='Admin', last_name='Admin', is_superuser=True)
        self.student_user = User.objects.create_user(username="stu-test", email="studenttest@test.com", password="student", first_name='Student', last_name='Student', is_student=True)
        self.instructor_user = User.objects.create_user(username="ins-test", email="instructortest@test.com", password="instructor", first_name='Instructor', last_name='Instructor', is_instructor=True)
        self.client_user = User.objects.create_user(username="client-test", email="clienttest@test.com", password="client", first_name='client', last_name='client', is_client=True)
        self.student = Student.objects.create(student=self.student_user, learning_style='visual')
        self.instructor = Instructor.objects.create(instructor=self.instructor_user, bio="Great Teacher!", experience=4, education="Google Certified", certifications="Python Advanced Certificate", rating=3.5, reviews=20000)
        self.program = Program.objects.create(title='Test Program', description='Test Program Description', price=19.99, duration=10)
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
        self.course = Course.objects.create(title='Test Course', description='Test Course Description', metadata=self.metadata, content=self.content, details=self.details)        
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Quiz Description', total_marks=10)
        self.question = Question.objects.create(quiz=self.quiz, text='Test Question', marks=2)
        self.answer = Answer.objects.create(question=self.question, text='Test Answer', is_correct=True)
        self.module = Module.objects.create(title='Test Module', description='Week 1 module', course=self.course, order=1, duration=4, quiz=self.quiz)
        self.lesson = Lesson.objects.create(module=self.module, title="First Lesson", content="First lesson Content", order=1, duration=15)
        self.video = Video.objects.create(title='Test Video', lesson=self.lesson, video_file='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.file = File.objects.create(title='Test File', description='This is a test file', lesson=self.lesson, file='file.txt')


class ProgramModelTestCase(APITestCaseSetUp):   
    def test_program_model(self):
        self.set_up()
        
        self.assertEqual(str(self.program), 'Test Program')
        self.assertEqual(self.program.get_short_description(), 'Test Program Description'[:500])
        self.assertTrue(isinstance(self.program, Program))


class CourseModelTestCase(APITestCaseSetUp):
    def test_course_model(self):
        self.set_up()
            
        self.assertEqual(str(self.course), 'Test Course')
        self.assertEqual(self.course.get_short_description(), 'Test Course Description'[:200] + '...')
        self.assertTrue(isinstance(self.course, Course))
        self.assertTrue(isinstance(self.course.metadata, CourseMetadata))
        self.assertTrue(isinstance(self.course.content, CourseContent))
        self.assertTrue(isinstance(self.course.details, CourseDetails))


class QuizModelTestCase(APITestCaseSetUp): 
    def test_quiz_model(self):
        self.set_up()
        
        self.assertEqual(str(self.quiz), 'Test Quiz')
        self.assertTrue(isinstance(self.quiz, Quiz))


class QuestionModelTestCase(APITestCaseSetUp):
    def test_question_model(self):
        self.set_up()

        self.assertEqual(str(self.question), 'Test Question')
        self.assertTrue(isinstance(self.question, Question))
        self.assertTrue(isinstance(self.question.quiz, Quiz))


class AnswerModelTestCase(APITestCaseSetUp):
    def test_answer_model(self):
        self.set_up()

        self.assertEqual(str(self.answer), 'Test Answer')


class ModuleModelTestCase(APITestCaseSetUp):
    def test_module_creation(self):
        self.set_up()

        self.assertEqual(self.module.title, 'Test Module')
        self.assertEqual(str(self.module), 'Test Module')
        self.assertEqual(self.module.description, 'Week 1 module')
        self.assertEqual(self.module.course, self.course)

    def test_module_order_cannot_be_negative(self):    
        self.set_up()

        # Test that the order of a Module cannot be negative
        with self.assertRaises(IntegrityError):
            module = Module.objects.create(title='Negative Order Module', description='A module with negative order', course=self.course, order=-1, duration=4, quiz=self.quiz)

    def test_module_duration_cannot_be_negative(self):
        self.set_up()

        # Test that the duration of a Module cannot be negative
        with self.assertRaises(IntegrityError):
            module = Module.objects.create(title='Negative Duration Module', description='A module with negative duration', course=self.course, order=2, duration=-4, quiz=self.quiz)


class LessonModelTestCase(APITestCaseSetUp):
    def test_lesson_creation(self):
        self.set_up()
        
        self.assertEqual(self.lesson.title, 'First Lesson')
        self.assertEqual(self.lesson.module, self.module)


class VideoModelTestCase(APITestCaseSetUp):
    def test_video_creation(self):
        self.set_up()

        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.lesson, self.lesson)
        self.assertEqual(self.video.video_file, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')


class FileModelTestCase(APITestCaseSetUp):   
    def test_file_creation(self):
        self.set_up()

        self.assertEqual(self.file.title, 'Test File')
        self.assertEqual(self.file.description, 'This is a test file')
        self.assertEqual(self.file.file, 'file.txt')
        self.assertEqual(self.file.lesson, self.lesson)


class EnrollmentModelTestCase(APITestCaseSetUp):
    def test_course_enrollment_creation(self):
        self.set_up()

        enrollment = Enrollment.objects.create(course=self.course, student=self.student)

        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.student, self.student)

    def test_enrollment_str(self):
        self.set_up()
        
        enrollment = Enrollment.objects.create(program=self.program, student=self.student)

        self.assertEqual(enrollment.program, self.program)
        self.assertEqual(enrollment.student, self.student)
        
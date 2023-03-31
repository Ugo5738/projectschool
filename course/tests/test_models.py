from accounts.models import User
from course.models import (Answer, Course, CourseContent, CourseDetails,
                           CourseMetadata, Enrollment, File, Lesson, Module,
                           Program, Question, Quiz, Video)
from django.db import IntegrityError
from membership.models import Instructor, Student
from project.models import Project, TechSkill
from rest_framework.test import APITestCase


class APITestCaseSetUp(APITestCase):
    def set_up(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="testing", first_name='Jane', last_name='Doe')
        self.instructor = Instructor.objects.create(instructor=self.user, bio="Great Teacher!", experience=4, education="Google Certified", certifications="Python Advanced Certificate", rating=3.5, reviews=20000)
        self.student = Student.objects.create(student=self.user, learning_style='visual')
        self.program = Program.objects.create(title='Test Program', description='Test Program Description', price=19.99, duration=10)
        self.skill = TechSkill.objects.create(name='Python')
        self.project = Project.objects.create(title='Project 1', description='Project 1 Description')
        self.metadata = CourseMetadata.objects.create(level='beginner', rating=4.5, price=9.99, certificate=True)
        self.content = CourseContent.objects.create(syllabus='Course Syllabus', prerequisites='Have a basic understanding of coding.')
        self.details = CourseDetails.objects.create(instructor=self.instructor, program=self.program, skills=self.skill, projects=self.project)
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
        
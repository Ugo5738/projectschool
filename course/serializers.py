from course.models import (Answer, Course, CourseContent, CourseDetails,
                           CourseMetadata, Lesson, Module, Program, Question,
                           Quiz)
from rest_framework import serializers


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class CourseMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMetadata
        fields = '__all__'


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = '__all__'


class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    metadata = CourseMetadataSerializer()
    content = CourseContentSerializer()
    details = CourseDetailsSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    quiz = QuizSerializer()
    lessons = serializers.StringRelatedField(many=True)

    class Meta:
        model = Module
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'

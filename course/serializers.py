from course.models import (Answer, Course, CourseContent, CourseDetails,
                           CourseMetadata, Lesson, Module, Program, Question,
                           Quiz, Video)
from project.models import TechSkill
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

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        content_data = validated_data.pop('content')
        details_data = validated_data.pop('details')
        skills_data = details_data.pop('skills', [])

        # Create the nested models
        metadata = CourseMetadata.objects.create(**metadata_data)
        content = CourseContent.objects.create(**content_data)
        details = CourseDetails.objects.create(**details_data)

        # Create the course with the nested models
        course = Course.objects.create(metadata=metadata, content=content, details=details, **validated_data)

        # Add skills to the course details
        for skill_data in skills_data:
            skill = TechSkill.objects.get_or_create(id=skill_data.id)
            details.skills.add(skill_data)

        return course

        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  # , read_only=True)
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  # , read_only=True)
    lesson_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = Module
        fields = '__all__'

    def create(self, validated_data):
        lesson_ids = validated_data.pop('lesson_ids', [])
        module = Module.objects.create(**validated_data)

        # Attach the lessons to the module
        for lesson_id in lesson_ids:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                lesson.module = module
                lesson.save()
            except Lesson.DoesNotExist:
                pass

        return module
    
    
class LessonSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Video
        fields = '__all__'
from accounts.models import User
from project import models
from rest_framework import serializers


class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechSkill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField(required=False)

    class Meta:
        model = models.Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class ProjectAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectAttachment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectAttachment
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'
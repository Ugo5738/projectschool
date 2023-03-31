from project import models
from rest_framework import serializers


class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechSkill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'

from membership import models
from project.serializers import ProjectSerializer, TechSkillSerializer
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    tech_skills = TechSkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)

    class Meta:
        model = models.Student
        fields = '__all__'

    def update(self, instance, validated_data):
        tech_skills_data = validated_data.pop('tech_skills', None)
        projects_data = validated_data.pop('projects', None)

        if tech_skills_data:
            instance.tech_skills.set([models.TechSkill.objects.get_or_create(**data)[0] for data in tech_skills_data])
        
        if projects_data:
            instance.projects.set([models.Project.objects.get_or_create(**data)[0] for data in projects_data])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance


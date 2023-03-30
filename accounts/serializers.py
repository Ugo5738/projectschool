from rest_framework import serializers

from . import models


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = models.User
        # fields = '__all__'
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


# wrong
# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=128, min_length=6, write_only=True)

#     class Meta:
#         model = models.User
#         # fields = ('username', 'email', 'password', 'token',)
#         fields = ('email', 'password')

#         read_only_fields = ['token']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

        
class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechSkill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


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


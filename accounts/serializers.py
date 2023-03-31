from accounts import models
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = models.User
        # fields = '__all__'
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


# wrong
# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=128, min_length=6, write_only=True)

#     class Meta:
#         model = models.User
#         # fields = ('username', 'email', 'password', 'token',)
#         fields = ('email', 'password')

#         read_only_fields = ['token']

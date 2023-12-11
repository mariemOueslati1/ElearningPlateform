# serializers.py
from rest_framework import serializers
from .models import UserProfile

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'roleList']

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        validated_data.pop('password2')

        user = super().create(validated_data)
        user.set_password(password1)
        user.save()
        return user



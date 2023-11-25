from rest_framework import serializers
from .models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.ReadOnlyField(source='course.id')
    class Meta:
        model = Assignment
        fields = '__all__'

from rest_framework import serializers
from .models import Enrollment
from courseApp.serializers import CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.id')
    course = serializers.ReadOnlyField(source='course.id')
    student_username = serializers.ReadOnlyField(source='student.username')
    course_title = serializers.ReadOnlyField(source='course.title')
    course_description = serializers.ReadOnlyField(source='course.description')

    class Meta:
        model = Enrollment
        fields ='__all__'


from rest_framework import serializers
from .models import Enrollment
from courseApp.serializers import CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.id')
    course = serializers.ReadOnlyField(source='course.id')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']


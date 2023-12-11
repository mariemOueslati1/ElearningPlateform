from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    assignment= serializers.ReadOnlyField(source='assignment.id')
    class Meta:
        model = Submission
        fields = '__all__'

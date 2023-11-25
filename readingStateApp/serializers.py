from rest_framework import serializers
from .models import ReadingState

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingState
        fields = [ 'read_state', 'last_read_date']

class ReadingStateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingState
        fields = '__all__'

from rest_framework import serializers
from .models import InteractionHistory

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionHistory
        exclude = ['interaction_type', 'student', 'material']

class InteractionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionHistory
        fields = '__all__'
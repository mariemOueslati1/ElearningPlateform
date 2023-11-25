from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    course = serializers.ReadOnlyField(source='course.id')
    class Meta:
        model = Material
        fields = '__all__'

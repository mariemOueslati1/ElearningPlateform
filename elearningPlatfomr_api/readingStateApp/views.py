from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ReadingState
from .serializers import ReadingSerializer , ReadingStateListSerializer
from interactionApp.permissions import IsStudent
from django.shortcuts import render
class ReadingStateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticated , IsStudent ]

    def get_queryset(self):
        # Retrieve the reading state for the authenticated user and specified material
        return ReadingState.objects.filter(student=self.request.user)

    def get_object(self):
        # Get the existing reading state for the authenticated user and specified material
        queryset = self.get_queryset()
        material_id = self.kwargs.get('material_id')
        return queryset.filter(material_id=material_id).first()

    def perform_create(self, serializer):
        # Set the student field to the authenticated user
        material_id = self.kwargs.get('material_id')
        serializer.save(student=self.request.user, material_id=material_id)

    def perform_update(self, serializer):
        # Update the existing reading state for the authenticated user and specified material
        material_id = self.kwargs.get('material_id')
        serializer.save(student=self.request.user, material_id=material_id)

class ListReadingStatesView(generics.ListAPIView):
    serializer_class = ReadingStateListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve all reading states for the authenticated user
        return ReadingState.objects.filter(student=self.request.user)

    def render_read_states(self, queryset):
        # Customize this function to render the readStates.html template
        context = {'reading_states': queryset}
        return render(self.request, 'reads.html', context)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.render_read_states(queryset)
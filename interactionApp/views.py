from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import InteractionHistory
from .serializers import InteractionSerializer , InteractionListSerializer
from django.shortcuts import get_object_or_404
from MaterialApp.models import Material
from rest_framework.response import Response
from rest_framework import status
from .permissions  import IsStudent
from rest_framework.generics import CreateAPIView
# Create your views here.
class AddInteractionView(CreateAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_material(self, material_id):
        return get_object_or_404(Material, pk=material_id)

    def perform_create(self, serializer):
        material_id = self.kwargs.get('material_id')
        interaction_type = self.kwargs.get('interaction_type')
        material = self.get_material(material_id)
        serializer.save(
            student=self.request.user,
            material=material,
            interaction_type=interaction_type
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # You can also return the serialized data in the response if needed
        response_serializer = self.get_serializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class ListInteractionsView(generics.ListAPIView):
    serializer_class = InteractionListSerializer
    permission_classes = [IsAuthenticated, IsStudent]  # Adjust permissions as needed

    def get_queryset(self):
        # Retrieve all interactions for the authenticated student
        return InteractionHistory.objects.filter(student=self.request.user)
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
    permission_classes = [IsAuthenticated]

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
        print("Inside AddInteractionView post method")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Log or print received data for debugging
        print("Received Material ID:", kwargs.get('material_id'))
        print("Received Interaction Type:", kwargs.get('interaction_type'))
        print("Received Data:", serializer.validated_data)

        self.perform_create(serializer)

        # You can also return the serialized data in the response if needed
        response_serializer = self.get_serializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

class ListInteractionsView(generics.ListAPIView):
    serializer_class = InteractionListSerializer
    permission_classes = [IsAuthenticated,IsStudent]  

    def get_queryset(self):
        # Extract material_id from the URL
        material_id = self.kwargs.get('material_id')

        # Set student_id as the same as the request user
        student_id = self.request.user.id

        # Your logic to filter queryset based on material_id and student_id
        queryset = InteractionHistory.objects.filter(material_id=material_id, student=student_id)

        # You may adjust the filtering logic based on your specific requirements

        return queryset

    def get(self, request, *args, **kwargs):
        # Call the get_queryset method to get the filtered queryset
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)

        # Render the HTML template with the serialized data
        return render(request, 'interactions.html', {'interactions': serializer.data})
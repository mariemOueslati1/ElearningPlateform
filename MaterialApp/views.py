from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Material
from .serializers import MaterialSerializer
from rest_framework.permissions import IsAuthenticated
from courseApp.models import Course 
from rest_framework.serializers import ValidationError
from django.http import Http404

from .permissions import CanUploadMaterialPermission , IsCourseTutor
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404

# Create your views here.


class AddMaterialView(APIView):
    permission_classes = [IsAuthenticated , CanUploadMaterialPermission , IsCourseTutor]

    def get_course(self, course_id):
        try:
            return Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise ValidationError('Course with the specified ID does not exist.')

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        course = self.get_course(course_id)
        print ("course_id: ", course_id)

        # Ensure that the requesting user is the tutor of the course
        if request.user != course.tutor:
            raise PermissionDenied("You do not have permission to add materials to this course.")

        serializer = MaterialSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(course=course)
            return Response({'detail': 'Material added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMaterialView(generics.UpdateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]

    def get_object(self):
        material_id = self.kwargs.get('material_id')
        try:
            return get_object_or_404(Material, pk=material_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Material  did not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, *args, **kwargs):
        material_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(material_or_response, Response):
            return material_or_response

        material = material_or_response

        print("request user:", request.user)
        print("material course tutor id:", material.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != material.course.tutor:
            error_msg = "You do not have permission to update this material."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(material, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'detail': 'Material updated successfully.'}, status=status.HTTP_200_OK)
    
class DeleteMaterialView(generics.DestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]

    def get_object(self):
        material_id = self.kwargs.get('material_id')
        try:
            return get_object_or_404(Material, pk=material_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Material  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        material_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(material_or_response, Response):
            return material_or_response

        material = material_or_response

        print("request user:", request.user)
        print("material course tutor id:", material.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != material.course.tutor:
            error_msg = "You do not have permission to update this material."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)


        material.delete()
        return Response({'detail': 'Material deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ListMaterialView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        return Material.objects.filter(course=course)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serialize the queryset and return the response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MaterialDetailView(generics.RetrieveAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        material_id = self.kwargs.get('material_id')
        try:
            return get_object_or_404(Material, pk=material_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Material  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print("instance: " , instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
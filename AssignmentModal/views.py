from django.shortcuts import render , get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework.permissions import IsAuthenticated
from courseApp.models import Course 
from MaterialApp.permissions import IsCourseTutor ,  CanUploadMaterialPermission
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
# Create your views here.
class AddAssignmentView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsCourseTutor , CanUploadMaterialPermission]

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

        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(course=course)
            return Response({'detail': 'Assignment added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListAssignmentView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        return Assignment.objects.filter(course=course)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serialize the queryset and return the response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateAssignmentView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]

    def get_object(self):
        assignment_id = self.kwargs.get('assignment_id')
        try:
            return get_object_or_404(Assignment, pk=assignment_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Assignment  did not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, *args, **kwargs):
        assignment_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(assignment_or_response, Response):
            return assignment_or_response

        assignment = assignment_or_response

        print("request user:", request.user)
        print("material course tutor id:", assignment.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != assignment.course.tutor:
            error_msg = "You do not have permission to update this assignement."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(assignment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'detail': 'Assignment updated successfully.'}, status=status.HTTP_200_OK)
    
class DeleteAssignmentView(generics.DestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]

    def get_object(self):
        assignment_id = self.kwargs.get('assignment_id')
        try:
            return get_object_or_404(Assignment, pk=assignment_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Assignment  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        assignment_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(assignment_or_response, Response):
            return assignment_or_response

        assignment = assignment_or_response

        print("request user:", request.user)
        print("material course tutor id:", assignment.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != assignment.course.tutor:
            error_msg = "You do not have permission to update this assignement."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)



        assignment.delete()
        return Response({'detail': 'Assignemnt deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
from django.shortcuts import render , get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import SubmissionSerializer
from .models import Submission
from AssignmentModal.models import Assignment
from rest_framework.serializers import ValidationError
from .permissions import CanUpsubmitAssignment
from .serializers import SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
# Create your views here.
class AddSubmissionView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated , CanUpsubmitAssignment]

    def get_assignment(self, assignment_id):
        try:
            return Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            raise ValidationError('Assignment with the specified ID does not exist.')

    def post(self, request, *args, **kwargs):
        # Extract assignment_id from the URL
        assignment_id = self.kwargs.get('assignment_id')

        # Get the assignment
        assignment = self.get_assignment(assignment_id)

        # Automatically set the student field based on the authenticated user
        request.data['student'] = request.user.id

        # Ensure that the assignment is associated with the correct course or any other necessary checks
        # You might need to adjust this based on your models and requirements

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assignment=assignment)
            return Response({'detail': 'Submission added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateSubmissionView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, CanUpsubmitAssignment]

    def get_object(self):
        submission_id = self.kwargs.get('submission_id')
        try:
            return get_object_or_404(Submission, pk=submission_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Submission  did not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, *args, **kwargs):
        submission_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance( submission_or_response, Response):
            return  submission_or_response

        submission =  submission_or_response

        print("request user:", request.user)
        print("submission student  id:", submission.student)

        # Check if the requesting user is the tutor of the course
        if request.user != submission.student:
            error_msg = "You do not have permission to update this submission."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'detail': 'Submission updated successfully.'}, status=status.HTTP_200_OK)


class DeleteSubmissionView(generics.DestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, CanUpsubmitAssignment]

    def get_object(self):
        submission_id = self.kwargs.get('submission_id')
        try:
            return get_object_or_404(Submission, pk=submission_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Submission  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        submission_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance( submission_or_response, Response):
            return  submission_or_response

        submission =  submission_or_response

        print("request user:", request.user)
        print("submission student  id:", submission.student)

        # Check if the requesting user is the tutor of the course
        if request.user != submission.student:
            error_msg = "You do not have permission to update this submission."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)


        submission.delete()
        return Response({'detail': 'Submission deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ListSubmissionView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        return Submission.objects.filter(assignment=assignment_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serialize the queryset and return the response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
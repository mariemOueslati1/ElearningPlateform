from django.shortcuts import render , get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from SubmissionApp.models import Submission
from .models import Grade
from rest_framework.serializers import ValidationError
from .permissions import evaluate_assignments_permission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .serializers import GradeSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# Create your views here.
class AddGradeView(APIView):
    permission_classes = [IsAuthenticated, evaluate_assignments_permission]

    def get_submission(self, submission_id):
        try:
            return Submission.objects.get(pk=submission_id)
        except Submission.DoesNotExist:
            raise ValidationError('Submission with the specified ID does not exist.')

    def post(self, request, *args, **kwargs):
        submission_id = self.kwargs.get('submission_id')
        submission = self.get_submission(submission_id)

        # Extract student_id from Submission and use it to set the student field in Grade
        student_id = submission.student_id
        assignment_id = submission.assignment_id

        # Add student and assignment data to the request.data
        request.data['student'] = student_id
        request.data['assignment'] = assignment_id

        # Create the serializer with the modified request.data
        serializer = GradeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Grade added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateGradeView(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, evaluate_assignments_permission]

    def get_object(self):
        grade_id = self.kwargs.get('grade_id')
        try:
            return get_object_or_404(Grade, pk=grade_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Grade id  did not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, *args, **kwargs):
        grade_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(grade_or_response, Response):
            return grade_or_response

        grade = grade_or_response

        

        serializer = self.get_serializer(grade, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'detail': 'Grade updated successfully.'}, status=status.HTTP_200_OK)

class DeleteGradeView(generics.DestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, evaluate_assignments_permission]

    def get_object(self):
        grade_id = self.kwargs.get('grade_id')
        try:
            return get_object_or_404(Grade, pk=grade_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Grade id  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        grade_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(grade_or_response, Response):
            return grade_or_response

        grade = grade_or_response
        grade.delete()
        return Response({'detail': 'Grade deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ListGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.request.query_params.get('assignment_id')
        print ('assignment_id ', assignment_id)
        student_id = self.request.query_params.get('student_id')

        queryset = Grade.objects.all()

        if assignment_id:
            try:
                queryset = queryset.filter(assignment_id=assignment_id)
            except Grade.DoesNotExist:
                raise Http404("Assignment ID does not exist.")

        if student_id:
            try:
                queryset = queryset.filter(student_id=student_id)
            except Grade.DoesNotExist:
                raise Http404("Student ID does not exist.")

        return queryset

        return queryset
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_id = self.kwargs.get('assignment_id')
        student_id = self.kwargs.get('student_id')

        # Check if assignment_id and student_id are provided in the URL
        if assignment_id and student_id:
            return Grade.objects.filter(assignment_id=assignment_id, student_id=student_id)
        elif assignment_id:
            return Grade.objects.filter(assignment_id=assignment_id)
        elif student_id:
            return Grade.objects.filter(student_id=student_id)
        else:
            return Grade.objects.all()           
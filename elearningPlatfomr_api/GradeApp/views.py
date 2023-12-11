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
from AssignmentModal.models import Assignment
from django.http import HttpResponse
import logging
from .forms import GradeForm
from django.template.response import TemplateResponse
class AddGradeView(APIView):
    permission_classes = [IsAuthenticated, evaluate_assignments_permission]

    logger = logging.getLogger(__name__)

    def get_assignment(self, assignment_id):
        try:
            return Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            self.logger.error('Assignment with the specified ID does not exist.')
            raise ValidationError('Assignment with the specified ID does not exist.')



    def post(self, request, *args, **kwargs):
        try:
            assignment_id = self.kwargs.get('assignment_id')
            assignment = self.get_assignment(assignment_id)

            # Add student and assignment data to the request.data
            
            request.data['assignment'] = assignment_id

            # Log the request data
            self.logger.info('Request Data: %s', request.data)

            # Create the serializer with the modified request.data
            serializer = GradeSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Grade added successfully.'}, status=status.HTTP_201_CREATED)
            else:
                self.logger.error('Serializer errors: %s', serializer.errors)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.logger.exception('An error occurred: %s', str(e))
            return Response({'detail': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateGradeView(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, evaluate_assignments_permission]

    lookup_field = 'pk' 
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            
            form = GradeForm(initial={
                'grade': instance.grade,
                'feedback': instance.feedback,
            })
            context = {'Grade': instance, 'form': form, 'gradeId': instance.id ,'assignment': instance.assignment.id}
            
            # Render the template for the GET request
            template_name = 'update_grade.html' 
            return TemplateResponse(request, template_name, context)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to update this grade.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        assignment_id = self.kwargs.get('assignment_id')
        print(assignment_id)
        queryset = Grade.objects.filter(assignment_id=assignment_id)
        # Check if the queryset is empty and raise Http404 if needed
        
        return queryset
    def get(self, request, *args, **kwargs):
        # Call the get_queryset method to get the filtered queryset
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)

        # Render the HTML template with the serialized data
        return render(request, 'grades/grades_list.html', {'grades': serializer.data})
class ListGradesViewStudent(generics.ListAPIView):

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Extract assignment_id from the URL
        assignment_id = self.kwargs.get('assignment_id')

        # Set student_id as the same as the request user
        student_id = self.request.user.id

        # Your logic to filter queryset based on assignment_id and student_id
        queryset = Grade.objects.filter(assignment_id=assignment_id, student_id=student_id)

        # Check if the queryset is empty and raise Http404 if needed
        if not queryset.exists():
            raise Http404("No grades found for the given assignment and student.")

        return queryset

    def get(self, request, *args, **kwargs):
        # Call the get_queryset method to get the filtered queryset
        queryset = self.get_queryset()

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)

        # Render the HTML template with the serialized data
        return render(request, 'grades/grades_list.html', {'grades': serializer.data})
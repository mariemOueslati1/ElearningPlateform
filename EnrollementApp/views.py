from django.shortcuts import render , get_object_or_404
from rest_framework import generics , serializers, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated 
from .permissions import enroll_permission , IsEnrollmentOwner
from django.core.exceptions import PermissionDenied
from courseApp.models import Course
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class EnrollmentListView(generics.ListAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def list(self, request, *args, **kwargs):
        try:
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return Response({'error': 'User must be authenticated to view enrollments.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Filter the queryset to show only the enrollments of the current user
            queryset = self.get_queryset().filter(student=request.user)

            # Check if there are any enrollments
            if not queryset.exists():
                return Response({'detail': 'No enrollments available.'}, status=status.HTTP_204_NO_CONTENT)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated , enroll_permission] 

    def get_course(self, course_id):
        return get_object_or_404(Course, id=course_id)

    def perform_create(self, serializer):
        try:
            course_id = self.kwargs.get('course_id')
            course = self.get_course(course_id)
            serializer.save(student=self.request.user, course=course)
        except PermissionDenied:
            raise serializers.ValidationError('You do not have permission to enroll in this course.')
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'request': self.request}


class EnrollmentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated , enroll_permission , IsEnrollmentOwner]

    def destroy(self, request, *args, **kwargs):
        try:
            # Check if the enrollment exists
            instance = self.get_object()
             # Logging instead of print
            logger.debug(f"Authenticated User ID: {request.user.id}")
            logger.debug(f"Enrollment Student ID: {instance.student.id}")
            instance.delete()
            return Response({'detail': 'Enrollment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#didn't tested
class EnrollmentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, enroll_permission , IsEnrollmentOwner]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'detail': 'Enrollment updated successfully.'}, status=status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
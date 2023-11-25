from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
# Create your views here.
from rest_framework import generics , permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.serializers import ValidationError
from django.core.exceptions import PermissionDenied
from courseApp.models import Course
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course
from .serializers import CourseSerializer
from  .permissions import CanUpdateCoursePermission , CanDeleteCoursePermission
from elearningApp.models import UserProfile
import smtplib
class AddCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, CanUpdateCoursePermission]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Include the tutor field before calling is_valid
        request.data['tutor'] = request.user.id
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to create a course.'}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def perform_create(self, serializer):
        # Set the tutor field to the ID of the authenticated user
        serializer.save(tutor=self.request.user)
    
        # Notify all students about the new course
        self.notify_students(Course)

    def notify_students(self, course):
    # Fetch all users with roleList == 'Student'
        students = UserProfile.objects.filter(roleList='Student')
        print("Student : ", students)
        # Send email to each student
        for student in students:
            self.send_notification_email(student.email, course)
    @staticmethod
    def test_email_connection():
        try:
            # Establish a connection to the SMTP server
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)

            # Start TLS (Transport Layer Security) if configured
            if settings.EMAIL_USE_TLS:
                server.starttls()

            # Login to the SMTP server with your Gmail credentials
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Close the connection
            server.quit()

            print("Connection to Gmail SMTP server established successfully.")
        except Exception as e:
            print(f"Failed to establish connection to Gmail SMTP server. Error: {str(e)}")


    def send_notification_email(self, recipient_email, course):
        # Call the function to test the connection
        self.test_email_connection()
        """
        subject = 'New Course Added'
        message = f"Dear student,\n\nA new course '{course.title}' has been added. Check it out on our platform!"
        from_email = settings.EMAIL_HOST_USER
        try:
            # Attempt to send the email
            send_mail(subject, message, from_email, [recipient_email])
            print(f"Email sent successfully to {recipient_email}")
            return Response({'detail': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle the exception (e.g., log the error)
            print(f"Failed to send email to {recipient_email}. Error: {str(e)}")
            return Response({'error': 'Failed to send email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        """
        

class DeleteCourseView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, CanDeleteCoursePermission]  

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response({'error': 'You do not have permission to create a course.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateCourseView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, CanUpdateCoursePermission] 

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Check if the user has permission to update the course
            self.check_object_permissions(request, instance)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({'detail': 'Course updated successfully.'}, status=status.HTTP_200_OK)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to update this course.'}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ListCoursesView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 
    permission_classes = [IsAuthenticated]  
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Get the list of courses
            courses = self.list(request, *args, **kwargs).data
            print("courses : ", courses)
            # Render the template with the list of courses and user information
            return render(request, 'course_list.html', {'courses': courses, 'user': request.user})
        else:
            # Handle unauthenticated users as needed
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)



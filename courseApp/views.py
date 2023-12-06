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
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveAPIView
from .forms import CourseForm
from django.template.response import TemplateResponse
from EnrollementApp.serializers import EnrollmentSerializer
from EnrollementApp.models import Enrollment
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
            preview_data = serializer.validated_data
            print("data: ", preview_data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to create a course.'}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

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

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            
            form = CourseForm(initial={
                'title': instance.title,
                'description': instance.description,
                'enrollment_capacity': instance.enrollment_capacity,
                'tutor': instance.tutor,
                
            })
            context = {'course': instance , 'form': form}
            
            # Render the template for the GET request
            template_name = 'update_course.html'  # Change this to your actual template name
            return TemplateResponse(request, template_name, context)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to update this course.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Return a response for the successful update
            return Response({'detail': 'Course updated successfully.'}, status=status.HTTP_200_OK)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to update this course.'}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = CourseSerializer 

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Get the list of courses
            courses = self.list(request, *args, **kwargs).data
            # Render the template with the list of courses and user information
            return render(request, 'course_list.html', {'courses': courses, 'user': request.user})
        else:
            # Handle unauthenticated users as needed
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

class TutorListCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        print("user_id = ", user_id)
        return Course.objects.filter(tutor_id=user_id)

    def get(self, request, *args, **kwargs):
        courses = self.list(request, *args, **kwargs).data
            # Render the template with the list of courses and user information
        return render(request, 'tutorDashboard.html', {'courses': courses, 'user': request.user})

class StudentListCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        student_id = self.request.user.id
        return Enrollment.objects.filter(student_id=student_id).select_related('course')

    def get(self, request, *args, **kwargs):
        enrollments = self.list(request, *args, **kwargs).data
        return render(request, 'studentdashboard.html', {'enrollments': enrollments, 'user': request.user})

#for return only the course
class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = {'course': serializer.data}
        return render(request, 'course-details.html', context)
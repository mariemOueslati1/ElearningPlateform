# soap_service/views.py

from spyne import ServiceBase, rpc, Integer, ComplexModel, Float
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
import requests
from courseApp.models import Course
from EnrollementApp.models import Enrollment
from django.shortcuts import render
from spyne.model.primitive import Unicode, Float
from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.primitive import Double
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from spyne import Application, rpc, ServiceBase, Unicode, Integer
from django.shortcuts import render
from courseApp.models import Course
from django.db.models import Count
from spyne.client.http import HttpClient
from spyne.protocol.soap import Soap11

class AnalyticsService(ServiceBase):
    class EnrolledStudentCount(ComplexModel):
        __namespace__ = "AnalyticsService"
        enrollment_count = Float
        assignment_count = Float
        submission_count = Float

    @rpc(Integer, _returns=EnrolledStudentCount)
    def get_enrolled_student_count(ctx, course_id):
        try:
            # Use annotate to count enrollments, assignments, and submissions for the specified course
            course = Course.objects.filter(id=course_id).annotate(
                enrollment_count=Count('enrollment'),
                assignment_count=Count('assignment'),
                submission_count=Count('assignment__submission')
            ).first()

            if course:
                # Print the measures before returning them
                print(f"Enrollment Count: {course.enrollment_count}, Assignment Count: {course.assignment_count}, Submission Count: {course.submission_count}")

                # Convert counts to float and return them
                result = AnalyticsService.EnrolledStudentCount(
                    enrollment_count=float(course.enrollment_count),
                    assignment_count=float(course.assignment_count),
                    submission_count=float(course.submission_count)
                )
                
                return result
            else:
                # Adjust the default values as needed
                return AnalyticsService.EnrolledStudentCount(enrollment_count=0.0, assignment_count=0.0, submission_count=0.0)
        except Course.DoesNotExist:
            # Adjust the default values as needed
            return AnalyticsService.EnrolledStudentCount(enrollment_count=0.0, assignment_count=0.0, submission_count=0.0)
from django.shortcuts import render
from zeep import Client

def get_enrolled_student_count(request, course_id):
    try:
        # Assuming AnalyticsService is the WSDL URL
        wsdl_url = "http://localhost:8000/soap_service/analytics/?wsdl"
        client = Client(wsdl_url)

        # Call the SOAP service method
        enrolled_student_count = client.service.get_enrolled_student_count(course_id)

        # Access the attributes of the EnrolledStudentCount instance
        enrollment_count = enrolled_student_count.enrollment_count

        assignment_count = enrolled_student_count.assignment_count
        submission_count = enrolled_student_count.submission_count
        print(submission_count)
        # Return the counts to the frontend
        return render(request, 'analytics.html', {
            'enrollment_count': enrollment_count,
            'assignment_count': assignment_count,
            'submission_count': submission_count,
        })
    except Exception as e:
        # Handle errors
        return render(request, 'analytics.html', {'error': str(e)})
    

from .utils import recognize_speech, process_user_response, get_student_names, initialize_attendance_status

def voice_call(request):
    if request.method == 'POST':
        user_response = recognize_speech()
        print("user response : ", user_response)

        student_names = get_student_names()
        attendance_status = initialize_attendance_status(student_names)

        attendance_status = process_user_response(user_response, attendance_status)
        for student, status in attendance_status.items():
            print(student, status)
        return render(request, 'result.html', {'attendance_status': attendance_status})
    else:
        return render(request, 'test.html')







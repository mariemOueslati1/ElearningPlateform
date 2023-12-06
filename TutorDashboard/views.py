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
        result = client.service.get_enrolled_student_count(course_id)

        # Return the result to the frontend
        return render(request, 'analytics.html', {'result': result})
    except Exception as e:
        # Handle errors
        return render(request, 'analytics.html', {'error': str(e)})
    
    






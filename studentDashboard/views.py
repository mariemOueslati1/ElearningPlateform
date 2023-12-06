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
from elearningApp.models import UserProfile
from AssignmentModal.models import Assignment


from django.shortcuts import render
from zeep import Client

# Define the SOAP service for the student
class StudentAnalyticsService(ServiceBase):
    class CourseMetrics(ComplexModel):
        __namespace__ = "StudentAnalyticsService"
        submitted_assignment_count = Float
        read_state_percentage = Float

    @rpc(Integer, Integer, _returns=CourseMetrics)
    def get_course_metrics(ctx, student_id, course_id):
        try:
            # Use annotate to count submitted assignments for the student and calculate read state percentage for the course
            student = UserProfile.objects.get(id=student_id)
            course = Course.objects.filter(id=course_id).first()

            if student and course:
                # Count submitted assignments
                submitted_assignment_count = Assignment.objects.filter(
                    course=course,
                    submission__student=student
                ).count()

                # Calculate read state percentage for the course (replace with your actual logic)
                # Here, we assume a placeholder value for demonstration purposes
                total_assignments_for_course = Assignment.objects.filter(course=course).count()
                read_state_percentage = (submitted_assignment_count / total_assignments_for_course) * 100

                # Print the measures before returning them
                print(f"Submitted Assignment Count: {submitted_assignment_count}, Read State Percentage: {read_state_percentage}%")

                # Convert counts to float and return them
                result = StudentAnalyticsService.CourseMetrics(
                    submitted_assignment_count=float(submitted_assignment_count),
                    read_state_percentage=float(read_state_percentage)
                )
                
                return result
            else:
                # Adjust the default values as needed
                return StudentAnalyticsService.CourseMetrics(submitted_assignment_count=0.0, read_state_percentage=0.0)
        except (UserProfile.DoesNotExist, Course.DoesNotExist):
            # Adjust the default values as needed
            return StudentAnalyticsService.CourseMetrics(submitted_assignment_count=0.0, read_state_percentage=0.0)

from django.shortcuts import render
from zeep import Client

def get_course_metrics(request, course_id):
    try:
        # Assuming your SOAP service is hosted at this URL
        wsdl_url = "http://localhost:8000/soap_serviceStudent/student_analytics/?wsdl"
        client = Client(wsdl_url)

        # Use the user id as the student id
        student_id = request.user.id

        # Call the SOAP service method
        soap_result = client.service.get_course_metrics(course_id, student_id)

        # Combine SOAP result with course details
        result = {
            'course_id': course_id,
            'soap_result': soap_result  # The result from the SOAP API
        }
        print ('result:', result)
        # Return the result to the frontend
        return render(request, 'course_metrics.html', {'result': result})
    except Exception as e:
        # Handle errors
        return render(request, 'course_metrics.html', {'error': str(e)})
    
    






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
from SubmissionApp.models import Submission

from django.shortcuts import render
from zeep import Client, exceptions

class StudentAnalyticsService(ServiceBase):
    class CourseMetrics(ComplexModel):
        __namespace__ = "StudentAnalyticsService"
        total_assignment_count = Float
        submitted_assignment_count = Float

    @rpc(Integer, Integer, _returns=CourseMetrics)
    def get_course_metrics(ctx, student_id, course_id):
        print("student id: " , student_id)
        try:
            student = UserProfile.objects.get(id=student_id)
            course = Course.objects.filter(id=course_id).first()

            if student and course:
                # Calculate total assignment count for the course
                total_assignment_count = Assignment.objects.filter(course=course).count()
                print("Total assignment count in class : ", total_assignment_count)

                # Count submitted assignments by the student
                submitted_assignment_count = Submission.objects.filter(
                    student=student,
                    assignment__course=course
                ).count()

                

                # Print the measures before returning them
                print(f"Total Assignment Count: {total_assignment_count}, Submitted Assignment Count: {submitted_assignment_count}")

                # Convert counts to float and return them
                result = StudentAnalyticsService.CourseMetrics(
                    total_assignment_count=float(total_assignment_count),
                    submitted_assignment_count=float(submitted_assignment_count),
                    
                )

                return result
            else:
                # Adjust the default values as needed
                return StudentAnalyticsService.CourseMetrics(
                    total_assignment_count=0.0,
                    submitted_assignment_count=0.0,
                    
                )
        except (UserProfile.DoesNotExist, Course.DoesNotExist):
            
            return StudentAnalyticsService.CourseMetrics(
                total_assignment_count=0.0,
                submitted_assignment_count=0.0,
                
            )


def get_course_metrics(request, course_id):
    try:
        # Assuming your SOAP service is hosted at this URL
        wsdl_url = "http://localhost:8000/soap_serviceStudent/student_analytics/?wsdl"
        
        try:
            client = Client(wsdl_url)
            
            # Check if the service description is available
            if client.wsdl.services:
                print("Connection established successfully.")
            else:
                print("No services found in the WSDL.")
        except Exception as e:
            print(f"Error connecting to the SOAP service: {e}")
        
        
        # Use the user id as the student id
        student_id = request.user.id
        print("Student :" , student_id)

        # Call the SOAP service method
        soap_result = client.service.get_course_metrics(student_id,course_id)
        print("soap_result :" , soap_result)

        # Extract data from the SOAP result
        total_assignment_count = soap_result.total_assignment_count
        print("Total assignments :", total_assignment_count)

        submitted_assignment_count = soap_result.submitted_assignment_count
        print ('Submitted assignments :', submitted_assignment_count)
        

        # Combine SOAP result with course details
        result = {
            'course_id': course_id,
            'total_assignment_count': total_assignment_count,
            'submitted_assignment_count': submitted_assignment_count,

        }
        print('result:', result)

        # Return the result to the frontend
        return render(request, 'course_metrics.html', {'result': result})
    except exceptions.Fault as e:
        # Handle SOAP Fault (Error returned by the SOAP service)
        return render(request, 'course_metrics.html', {'error': f"SOAP Fault: {e.message}"})
    except Exception as e:
        # Handle other exceptions
        return render(request, 'course_metrics.html', {'error': f"Error: {str(e)}"})
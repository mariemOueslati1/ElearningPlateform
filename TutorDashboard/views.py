# soap_service/views.py

from spyne import Application, rpc, ServiceBase
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

    @rpc(Integer, _returns=Float)  # Assuming the course_id is an integer
    def get_enrolled_student_count(ctx, course_id):
        try:
            # Use annotate to count enrollments for the specified course
            course = Course.objects.filter(id=course_id).annotate(enrollment_count=Count('enrollment')).first()

            if course:
                return float(course.enrollment_count)
            else:
                # Handle the case where the course is not found
                return 0.0  # Adjust the default value as needed
        except Course.DoesNotExist:
            # Handle the case where the course is not found
            return 0.0  # Adjust the default value as needed






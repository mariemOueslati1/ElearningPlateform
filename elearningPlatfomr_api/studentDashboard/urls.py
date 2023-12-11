from django.urls import path
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from .views import * 

urlpatterns = [
    path('student_analytics/', DjangoView.as_view(
        services=[StudentAnalyticsService],
        tns='analytics.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    ), name='student_analytics_wsdl'),
    path('get_course_metrics/<int:course_id>/', get_course_metrics, name='get_course_metrics'),
]
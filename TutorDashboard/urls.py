from django.urls import path
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from .views import * 

urlpatterns = [
    path('analytics/', DjangoView.as_view(
        services=[AnalyticsService],
        tns='analytics.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )),
    path('get_enrolled_student_count/<int:course_id>/', get_enrolled_student_count, name='get_enrolled_student_count'),
    
]

from django.urls import path
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from .views import AnalyticsService 

urlpatterns = [
    path('analytics/', DjangoView.as_view(
        services=[AnalyticsService],
        tns='analytics.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )),
    
]

from django.urls import path
from .views import voice_call

urlpatterns = [
    path('voice_call/', voice_call, name='voice_call'),
    
]

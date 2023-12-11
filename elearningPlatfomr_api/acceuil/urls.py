from django.urls import path
from .views import *

urlpatterns = [
    path('', acceuil_view, name='acceuil'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
]

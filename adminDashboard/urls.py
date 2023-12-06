# dashboard/urls.py
from django.urls import path
from .views import custom_dashboard_view

urlpatterns = [
    path('custom-dashboard/', custom_dashboard_view, name='custom_dashboard'),
]

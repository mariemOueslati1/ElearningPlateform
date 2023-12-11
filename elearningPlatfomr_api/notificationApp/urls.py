# urls.py
from django.urls import path
from .views import NotificationAPIView

urlpatterns = [
    path('api/notifications/', NotificationAPIView.as_view(), name='notification-api'),
    # Add your other URL patterns
]

# urls.py
from django.urls import path
from .views import RegistrationAPIView , LoginAPIView , LogoutAPI



urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
]

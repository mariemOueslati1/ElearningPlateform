from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm , CustomAuthenticationForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.views import LoginView
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.urls import reverse

from django.contrib.auth import logout as django_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@permission_classes([AllowAny])

class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate and save user registration
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the username or email already exists
            username_exists = UserProfile.objects.filter(username=serializer.validated_data['username']).exists()
            email_exists = UserProfile.objects.filter(email=serializer.validated_data['email']).exists()

            if username_exists:
                return Response({'error': 'Username is already taken. Please choose a different one.'}, status=status.HTTP_400_BAD_REQUEST)
            elif email_exists:
                return Response({'error': 'Email is already registered. Please use a different email.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return Response({'success': 'Registration successful. You can now log in.'}, status=status.HTTP_200_OK) 
        else:
            print(serializer.errors)
            return Response({'error': 'Form submission failed. Please check the form for errors.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Render the registration form template
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        print("username : " + username + " password : " + password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('list_courses')

        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        # Render the login form template
        form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Logout the user
        
        django_logout(request)
        # Redirect to the login page
        login_url = reverse('login')
        return redirect(login_url)

# your_app/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

class CustomAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/custom_admin.html'

    def test_func(self):
        # Check if the user is staff
        return self.request.user.is_staff
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
from rest_framework.authentication import TokenAuthentication
from django.urls import reverse
from rest_framework.authtoken.views import ObtainAuthToken
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

        user = authenticate(request, username=username, password=password)
        print("user : ", user)
        print("username : ",user.username)
        print("password : ",user.password)
        if user is not None:
            login(request, user)

            # Generate or get the authentication token
            token, created = Token.objects.get_or_create(user=user)
            print("token  : ",token)
            
            return Response({'success': 'login Successfully'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
    def get(self, request, *args, **kwargs):
        # Render the registration form template
        form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
"""
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print("request.user: ", request.user)
        try:
            # Get the user's authentication token
            token = Token.objects.get(user=request.user)
            print("token: ", token)

            # Delete the token to invalidate it
            token.delete()
            
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # Token not found, the user is effectively already logged out
            return Response({'detail': 'User is already logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Extract the token key from the Authorization header
        auth_header = request.headers.get('Authorization')
        print("auth header ", auth_header)
        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            print("token key ", token_key)
            # Delete the token to log the user out
            Token.objects.filter(key=token_key).delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        else:
            
            return Response({'error': 'Invalid or missing Authorization header.'}, status=status.HTTP_401_UNAUTHORIZED)"""

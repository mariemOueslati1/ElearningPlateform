from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2','roleList']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
"""
URL configuration for elearningPlatfomr_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from elearningApp.views import CustomAdminView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom_admin/', CustomAdminView.as_view(), name='custom_admin'),
    path('user/', include('elearningApp.urls')),
    path('', include('acceuil.urls')),
    path('courses/', include('courseApp.urls')),
    path('enrollments/', include('EnrollementApp.urls')),
    path('Material/',include('MaterialApp.urls')),
    path('Assignment/', include('AssignmentModal.urls')),
    path('Submission/', include('SubmissionApp.urls')),
    path('Grade/', include('GradeApp.urls')),
    path('Interaction/', include('interactionApp.urls')),
    path('Readings/', include('readingStateApp.urls')),
    path('soap_service/', include('TutorDashboard.urls')),
    path('soap_serviceStudent/', include('studentDashboard.urls')),
    path('nortifications/',include('notificationApp.urls')),
]

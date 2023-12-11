from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions 
# Create your views here.
class NotificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        data = [
            {
                "message": notification.message,
                "course_name": notification.course.title,
                "timestamp": notification.timestamp
            }
            for notification in notifications
        ]
        context = {'notifications': data}
        return render(request, 'notificationApp/notifications.html', context)

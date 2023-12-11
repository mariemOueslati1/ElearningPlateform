from django.urls import path
from .views import *

urlpatterns = [
    path('assignment/add/<int:course_id>/', AddAssignmentView.as_view(), name='add-assignment'),
    path('assignment/assignmentList/<int:course_id>/',ListAssignmentView.as_view(), name='assignment-list'),
    path('assignments/<int:assignment_id>/delete/', DeleteAssignmentView.as_view(), name='delete-assignment'),
    path('assignments/<int:pk>/update/', UpdateAssignmentView.as_view(), name='update-assignment'),

   
]

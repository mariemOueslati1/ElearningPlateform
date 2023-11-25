from django.urls import path
from .views import AddAssignmentView , ListAssignmentView

urlpatterns = [
    path('assignment/add/<int:course_id>/', AddAssignmentView.as_view(), name='add-assignment'),
    path('assignment/assignmentList/<int:course_id>/',ListAssignmentView.as_view(), name='assignment-list'),
   
]

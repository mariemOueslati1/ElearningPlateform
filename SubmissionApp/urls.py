from django.urls import path
from .views import AddSubmissionView , UpdateSubmissionView , DeleteSubmissionView , ListSubmissionView

urlpatterns = [

    # Add other URL patterns as needed
    path('submission/add/<int:assignment_id>/', AddSubmissionView.as_view(), name='add-submission'),
    path('submission/<int:submission_id>/update/', UpdateSubmissionView.as_view(), name='update-submission'),
    path('submission/<int:submission_id>/delete/', DeleteSubmissionView.as_view(), name='delete-submission'),
    path('submission/submitList/<int:assignment_id>/',ListSubmissionView.as_view(), name='submission-list'),
    
]

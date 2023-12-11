# urls.py
from django.urls import path
from .views import EnrollmentListView , EnrollmentCreateView , EnrollmentDetailView ,EnrollmentUpdateView , ListEnrollmentsByCourseView

urlpatterns = [
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('addEnrollment/<course_id>', EnrollmentCreateView.as_view(), name = 'enrollment_create'),
    path('enrollments/<course_id>', ListEnrollmentsByCourseView.as_view(), name = 'enrollments_for_course'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/update/', EnrollmentUpdateView.as_view(), name='enrollment_update'),

    
]

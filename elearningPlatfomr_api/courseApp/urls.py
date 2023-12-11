from django.urls import path
from .views import  *

urlpatterns = [
    path('add_course/', AddCourseView.as_view(), name='add_course'),
    path('courseList/', ListCoursesView.as_view(), name='list_courses'),
    path('tutor-courses/', TutorListCoursesView.as_view(), name='tutor-courses'),
    path('student-courses/', StudentListCoursesView.as_view(), name='student-courses'),
    path('courses/<int:pk>/', DeleteCourseView.as_view(), name='course-delete'),
    path('courses/update/<int:pk>/', UpdateCourseView.as_view(), name='course-update'),
    path('coursesDetails/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
]



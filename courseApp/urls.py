from django.urls import path
from .views import  ListCoursesView , DeleteCourseView ,AddCourseView , UpdateCourseView , TutorListCoursesView

urlpatterns = [
    path('add_course/', AddCourseView.as_view(), name='add_course_api'),
    path('courseList/', ListCoursesView.as_view(), name='list_courses'),
    path('TutorcourseList/', TutorListCoursesView.as_view(), name='TutorListCoursesView'),
    path('courses/<int:pk>/', DeleteCourseView.as_view(), name='course-delete'),
    path('courses/update/<int:pk>/', UpdateCourseView.as_view(), name='course-update')

]

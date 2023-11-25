from django.urls import path
from .views import  ListCoursesView , DeleteCourseView ,AddCourseView , UpdateCourseView

urlpatterns = [
    path('add_course/', AddCourseView.as_view(), name='add_course_api'),
    path('courseList/', ListCoursesView.as_view(), name='course-list'),
    path('courses/<int:pk>/', DeleteCourseView.as_view(), name='course-delete'),
    path('courses/update/<int:pk>/', UpdateCourseView.as_view(), name='course-update')

]

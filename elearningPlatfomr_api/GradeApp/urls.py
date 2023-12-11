from django.urls import path
from .views import *

urlpatterns = [

    # Add other URL patterns as needed
    path('grade/add/<int:assignment_id>/', AddGradeView.as_view(), name='add-grade'),
    path('grade/update/<int:pk>/', UpdateGradeView.as_view(), name='update-grade'),
    path('grade/delete/<int:grade_id>/', DeleteGradeView.as_view(), name='delete-grade'),
    path('Grade/Grade/grades/<int:assignment_id>/', ListGradesView.as_view(), name='list_grades'),
    path('Grade/Grade/grades/<int:assignment_id>/', ListGradesViewStudent.as_view(), name='list_gradesStudent'),



]

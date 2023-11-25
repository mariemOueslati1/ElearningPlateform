from django.urls import path
from .views import AddGradeView , UpdateGradeView , DeleteGradeView ,ListGradesView

urlpatterns = [

    # Add other URL patterns as needed
    path('grade/add/<int:submission_id>/', AddGradeView.as_view(), name='add-grade'),
    path('grade/update/<int:grade_id>/', UpdateGradeView.as_view(), name='update-grade'),
    path('grade/delete/<int:grade_id>/', DeleteGradeView.as_view(), name='delete-grade'),
    path('grades/gradesList/', ListGradesView.as_view(), name='list-grades'),

]
"""
    /api/grades/ - List all grades
/api/grades/?assignment_id=<assignment_id> - List grades by assignment
/api/grades/?student_id=<student_id> - List grades by student
    """

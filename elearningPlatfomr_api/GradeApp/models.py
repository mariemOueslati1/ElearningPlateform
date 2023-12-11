from django.db import models
from elearningApp.models import UserProfile
from AssignmentModal.models import Assignment

# Create your models here.
class Grade(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField()

    def __str__(self):
        return f"Grade for {self.assignment.title} by {self.student.username}"

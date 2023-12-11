from django.db import models
from elearningApp.models import UserProfile
from AssignmentModal.models import Assignment

# Create your models here.
class Submission(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) 
    submission_content = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.assignment.title}"
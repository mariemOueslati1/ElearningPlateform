from django.db import models
from courseApp.models import Course
from elearningApp.models import UserProfile


# Create your models here.
class Enrollment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    enrollment_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
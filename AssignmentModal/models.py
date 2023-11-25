from django.db import models
from courseApp.models import Course

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.title} for {self.course.title}"

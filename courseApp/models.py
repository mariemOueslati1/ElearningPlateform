from django.db import models
from elearningApp.models import UserProfile

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    enrollment_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

from django.db import models
from elearningApp.models import UserProfile
from MaterialApp.models import Material

# Create your models here.
class InteractionHistory(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    INTERACTION_TYPE_CHOICES = [
        ('upload', 'Upload'),
        ('read', 'Read'),
        # Add more interaction types as needed
    ]
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPE_CHOICES)
    interaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} {self.interaction_type} {self.material.title}"

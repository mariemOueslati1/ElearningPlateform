from django.db import models
from elearningApp.models import UserProfile
from MaterialApp.models import Material
# Create your models here.
class ReadingState(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.DecimalField(max_digits=5, decimal_places=2)  
    last_read_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} read {self.read_state}% of {self.material.title}"

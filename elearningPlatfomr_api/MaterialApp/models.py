from django.db import models
from courseApp.models import Course


# Create your models here.
class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Assuming the Course model is in the same app
    upload_date = models.DateTimeField(auto_now_add=True)
    
    DOCUMENT_TYPE_CHOICES = [
        ('PDF', 'PDF'),
        ('WORD', 'WORD'),  # Add more document types as needed
    ]
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} for {self.course.title}"

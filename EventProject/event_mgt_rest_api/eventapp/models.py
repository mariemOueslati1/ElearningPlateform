from django.db import models

# Create your models here.

class Event (models.Model):
    name = models.CharField(max_length=255,default="")
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=500,default="")
    time = models.TimeField(auto_now=True)
    url = models.URLField(null=True, blank=True)
    poster = models.ImageField(upload_to="images/")


#iiner class used to add or set the model metadata example : table name , some constraints like unique 
class Meta (models.Model):
    db_table = 'events'
    ordering = ['-date'] #descending
    unique_together = ['name', 'date','time']

def __str__(self):
    return f'Event(name= {self.name}, date= {self.date}, time= {self.time} )'


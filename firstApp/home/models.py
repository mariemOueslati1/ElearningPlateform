from django.db import models

class Student (models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True , null=True)
    adress = models.TextField()
    image = models.ImageField()
    file = models.FileField()

class Car(models.Model):
    car_name = models.CharField(max_length=500)
    speed = models.IntegerField(default=50)


    def __str__(self) -> str:
        return self.car_name 


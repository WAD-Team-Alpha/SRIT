from django.db import models
from .choices import *

# Create your models here.

class Student(models.Model):
    fn = models.CharField(max_length=100)
    ln = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    usr_nm = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10)
    sem_no = models.IntegerField(default=1)
    branch = models.CharField(choices=Department, default='CSE')

    def __str__(self):
        return self.roll_no

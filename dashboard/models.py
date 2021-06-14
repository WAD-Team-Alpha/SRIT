from django.db import models

# Create your models here.

class Marks(models.Model):
    type = models.IntegerField(default=0)
    sem_no = models.IntegerField(default=1)
    roll_no = models.CharField(max_length=10)
    s1 = models.IntegerField(default=0)
    s2 = models.IntegerField(default=0)
    s3 = models.IntegerField(default=0)
    s4 = models.IntegerField(default=0)
    s5 = models.IntegerField(default=0)
    s6 = models.IntegerField(default=0)
    s7 = models.IntegerField(default=0)
    s8 = models.IntegerField(default=0)

    def __str__(self):
        return self.roll_no

class Semester(models.Model):
    sem_no = models.IntegerField(default=1)
    roll_no = models.CharField(max_length=10)
    status = models.IntegerField(default=0)
    cst = models.IntegerField(default=0)
    ot = models.IntegerField(default=0)
    csp = models.IntegerField(default=0)
    op = models.IntegerField(default=0)
    s1 = models.CharField(blank=True)
    s2 = models.CharField(blank=True)
    s3 = models.CharField(blank=True)
    s4 = models.CharField(blank=True)
    s5 = models.CharField(blank=True)
    s6 = models.CharField(blank=True)
    s7 = models.CharField(blank=True)
    s8 = models.CharField(blank=True)

    def __str__(self):
        return self.roll_no
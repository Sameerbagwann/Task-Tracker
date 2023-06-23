from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=50)
    detail = models.CharField(max_length=255)
    cat = models.CharField(max_length=30)
    status=models.IntegerField()
    enddate=models.DateField()
    is_deleted=models.BooleanField(default=False)
    created_on=models.DateField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")

class verify(models.Model):
    gmail=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    otp=models.IntegerField()


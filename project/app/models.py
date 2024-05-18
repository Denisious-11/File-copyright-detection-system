from django.db import models

# Create your models here.
class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Files(models.Model):
    f_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    c_date=models.CharField(max_length=255)
    c_time=models.CharField(max_length=255)
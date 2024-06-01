# appointments/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nic_number = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)

class Doctor(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    nic_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


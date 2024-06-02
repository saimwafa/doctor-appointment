# appointments/models.py

# appointments/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nic_number = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    is_doctor = models.BooleanField(default=False)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    nic_number = models.CharField(max_length=20, unique=True)
    is_doctor = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.doctor.name} - {self.user.username}"


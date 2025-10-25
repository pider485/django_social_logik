from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Profile(AbstractUser):
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.username
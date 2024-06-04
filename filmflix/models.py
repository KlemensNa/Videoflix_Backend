from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    
class Video(models.Model):
    title = models.TextField(max_length=80)
    description = models.TextField(max_length=300)
    created_at = models.DateField(default=date.today)
    videos_file = models.FileField(upload_to="videos", blank=True, null=True)
    
    def __str__(self):
        return self.title





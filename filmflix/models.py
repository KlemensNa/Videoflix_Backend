from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

# AbstractUser is default User in Django
class CustomerUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    
class Video(models.Model):
    
    SPORT_CHOICES = [
        ('golf', 'Golf'),
        ('football', 'Fußball'),
        ('handball', 'Handball'),
        ('basketball', 'Basketball'),
        ('boxing', 'Boxen'),
        ('skate', 'Skateboard'),
        ('baseball', 'Baseball'),
        ('amFootball', 'American Football'),
    ]
    
    CATEGORY_CHOICES = [
        ("", ''),
        ('ussport', 'US-Sport'),
        ('ballsport', 'Ballsport'),
    ]
    
    title = models.TextField(max_length=80)
    description = models.TextField(max_length=300)
    created_at = models.DateField(default=date.today)
    videos_file = models.FileField(upload_to="videos", blank=False, null=False)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False, null=False)
    isplaying = models.BooleanField(default=False)
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES, default='', blank=False, null=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return self.title






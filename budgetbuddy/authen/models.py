from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures/', default='default_profile.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile Picture"

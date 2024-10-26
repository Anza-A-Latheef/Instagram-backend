from django.contrib.auth.models import AbstractUser, User
from django.db import models

class UserProfile(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/')
    likes = models.PositiveIntegerField(default=0) 
    caption = models.TextField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile,on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.user}'s post"
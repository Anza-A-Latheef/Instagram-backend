from django.contrib import admin

# instagramapp/admin.py

from django.contrib import admin
from .models import UserProfile, Post

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password','profile_picture') 

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'likes', 'caption')  


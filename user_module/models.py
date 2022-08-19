from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class UserHolidayInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_holiday')
    country = models.CharField(max_length=30)
    holiday_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_in_post_like_dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_in_post_like_dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

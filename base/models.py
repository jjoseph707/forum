from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Board(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    host = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.topic

class Post(models.Model):
    board = models.ForeignKey(Board,on_delete=models.CASCADE, null=True) #delete post when board deleted
    creator = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

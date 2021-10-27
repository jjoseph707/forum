from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.topic

class Post(models.Model):
    board = models.ForeignKey(Board,on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


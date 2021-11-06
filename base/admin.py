from django.contrib import admin

from .models import Board, Post, User

admin.site.register(User)
admin.site.register(Board)
admin.site.register(Post)
from django.forms import ModelForm
from .models import Board, Post

class BoardForm(ModelForm):
    class Meta:
        model=Board
        fields='__all__'

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields='__all__'
        exclude=['board','creator']
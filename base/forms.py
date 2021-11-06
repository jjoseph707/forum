from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Board, Post, User

class BoardForm(ModelForm):
    class Meta:
        model=Board
        fields='__all__'
        exclude = ['host']

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields='__all__'
        exclude=['board','creator']

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','email','bio','password1','password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email','bio']
    
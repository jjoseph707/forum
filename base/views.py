from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Board, Post, User
from .forms import BoardForm, PostForm, RegisterUserForm


def home(request):
    boards = Board.objects.all()
    context = {'boards':boards}
    return render(request,'base/home.html',context)

#user
def login_user(request):
    if request.method=="POST":
            email=request.POST.get("email")
            password=request.POST.get("password")

            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request,'#1 Incorrect credentials')
                return redirect('login')
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'#2 Incorrect credentials')
                return redirect('login')

    context={}
    return render(request,'base/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = user.name.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    content={'form':form}
    return render(request,'base/register.html',content)


#board
def board(request, pk):
    target_board = Board.objects.get(topic=pk)
    posts = Post.objects.filter(board__topic=pk).order_by('-created')

    context = {'board':target_board,'posts':posts}
    return render(request,'base/board.html',context)

def create_board(request):
    form = BoardForm()
    if request.method == 'POST': #post handling
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/board-form.html',context)

def edit_board(request,pk):
    board = Board.objects.get(topic=pk)
    form = BoardForm(instance=board)
    if request.method == 'POST':
        form=BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board',pk=board.topic)

    context={'form':form}
    return render(request,'base/board-form.html',context)

def delete_board(request,pk):
    board = Board.objects.get(topic=pk)
    if request.method == 'POST':
        board.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':board})

#post
def post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    title=pk
    context={'post':post,'title':title}
    return render(request,'base/post.html',context)

def create_post(request,pk):
    form = PostForm()
    user = User.objects.get(id=1) #change when users added in
    board = Board.objects.get(topic=pk)
    title=pk

    if request.method == 'POST':
        Post.objects.create(
            #autofill board + creator
            board=board,
            creator=user,
            title=request.POST.get('title'),
            content=request.POST.get('content')
        )
        return redirect('board',pk=pk)

    context={'form':form,'title':title}
    return render(request,'base/post-form.html',context)

def edit_post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    form = PostForm(instance=post)
    title=pk

    if request.method == 'POST':
        form=PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post',pk=pk,pk2=pk2)

    context={'form':form,'title':title}
    return render(request,'base/post-form.html',context)

def delete_post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    if request.method == 'POST':
        post.delete()
        return redirect('board',pk=pk)
    return render(request, 'base/delete.html', {'obj':post})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from .models import Board, Post, User, Comment
from .forms import BoardForm, PostForm, RegisterUserForm, UserForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    boards = Board.objects.filter(
        Q(topic__icontains=q) |
        Q(description__icontains=q)
        )

    #boards = Board.objects.all()
    context = {'boards':boards}
    return render(request,'base/home.html',context)

#user

def user_profile(request,pk):
    profile=User.objects.get(name=pk)
    context={'profile':profile}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def edit_profile(request,pk):
    profile = User.objects.get(name=pk)
    form = UserForm(instance=profile)

    if request.user != profile:
        return HttpResponse('You are not allowed here')


    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=pk)
    context={'form':form}
    return render(request,'base/edit-profile.html',context)

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
            user.username = user.name.lower()
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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    target_board = Board.objects.get(topic=pk)

    #filter posts by board then filter by search params
    posts = Post.objects.filter(board__topic=pk).order_by('-created')
    posts = posts.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    ).order_by('-created')

    context = {'board':target_board,'posts':posts}
    return render(request,'base/board.html',context)

@login_required(login_url='login')
def create_board(request):
    form = BoardForm()

    if request.method == 'POST': #post handling
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.host = request.user
            board.topic = board.topic.lower()
            board.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/board-form.html',context)

@login_required(login_url='login')
def edit_board(request,pk):
    board = Board.objects.get(topic=pk)
    form = BoardForm(instance=board)

    if request.user != board.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form=BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board',pk=board.topic)

    context={'form':form}
    return render(request,'base/board-form.html',context)

@login_required(login_url='login')
def delete_board(request,pk):
    board = Board.objects.get(topic=pk)

    if request.user != board.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        board.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':board})

#post
def post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    comments = post.comment_set.all().order_by('-created')

    #comment posting
    if request.method == "POST":
        comment = Comment.objects.create(
            creator = request.user,
            post = post,
            content = request.POST.get('content')
        )
        return redirect('post',pk=pk,pk2=pk2)


    title=pk
    context={'post':post,'title':title,'comments':comments}
    return render(request,'base/post.html',context)

@login_required(login_url='login')
def create_post(request,pk):
    form = PostForm()
    user = User.objects.get(id=request.user.id) #change when users added in
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

@login_required(login_url='login')
def edit_post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    form = PostForm(instance=post)
    title=pk

    if request.user != post.creator:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form=PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post',pk=pk,pk2=pk2)

    context={'form':form,'title':title}
    return render(request,'base/post-form.html',context)

@login_required(login_url='login')
def delete_post(request, pk, pk2):
    post = Post.objects.get(id=pk2)

    if request.user != post.creator:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        post.delete()
        return redirect('board',pk=pk)
    return render(request, 'base/delete.html', {'obj':post})

#comment

@login_required(login_url='login')
def delete_comment(request,pk,pk2,pk3):
    comment = Comment.objects.get(id=pk3)

    if request.user != comment.creator:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        comment.delete()
        return redirect('post',pk=pk,pk2=pk2)
    
    return render(request,'base/delete.html',{'obj':comment})
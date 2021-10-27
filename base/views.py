from django.shortcuts import render
from .models import Board, Post


def home(request):
    boards = Board.objects.all()
    context = {'boards':boards}
    return render(request,'base/home.html',context)

def board(request, pk):
    target_board = Board.objects.get(topic=pk)
    posts = Post.objects.filter(board__topic=pk) #

    context = {'board':target_board,'posts':posts}
    return render(request,'base/board.html',context)

def post(request, pk, pk2):
    post = Post.objects.get(id=pk2)
    context={'post':post}
    return render(request,'base/post.html',context)
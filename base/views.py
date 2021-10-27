from django.shortcuts import render

boards = [
    {'id':1,'topic':'random'},
    {'id':2,'topic':'finance'},
    {'id':3,'topic':'anime'},
]

def home(request):
    context = {'boards':boards}
    return render(request,'base/home.html',context)
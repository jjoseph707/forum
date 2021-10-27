from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    #boards
    path('board/<str:pk>/',views.board,name='board'),
    path('board/<str:pk>/<str:pk2>/',views.post,name='post')
]

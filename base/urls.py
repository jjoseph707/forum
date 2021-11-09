from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('template/',views.template,name='template'),
    #user
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('profile/<str:pk>/',views.user_profile,name='user-profile'),
    path('profile/edit/<str:pk>/',views.edit_profile,name='edit-profile'),
    #boards
    path('board/<str:pk>/',views.board,name='board'),
    path('create-board/',views.create_board,name='create-board'),
    path('edit-board/<str:pk>/',views.edit_board,name='edit-board'),
    path('delete-board/<str:pk>/',views.delete_board,name='delete-board'),
    #posts
    path('board/<str:pk>/<str:pk2>/',views.post,name='post'),
    path('create-post/<str:pk>/',views.create_post,name='create-post'),
    path('edit-post/<str:pk>/<str:pk2>/',views.edit_post,name='edit-post'),
    path('delete-post/<str:pk>/<str:pk2>/',views.delete_post,name='delete-post'),
    #comments
    path('delete-comment/<str:pk>/<str:pk2>/<str:pk3>/',views.delete_comment,name='delete-comment'),
]

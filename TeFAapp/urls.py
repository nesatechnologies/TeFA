from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('conformed/', views.conformed, name='conformed'),
    path('need_following/', views.need_following, name='need_following'),
    path('denied/', views.denied, name='denied'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_customer/<int:id>/', views.delete, name='delete'),
    path('call/<int:id>/', views.call, name='call'),
    path('followup/<int:id>/', views.followup, name='followup'),
    path('followup_actions/<int:id>/', views.followup_actions, name='followup_actions'),
    ]
from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('conformed/', views.conformed, name='conformed'),
    path('need_following/', views.need_following, name='need_following'),
    path('denied/', views.denied, name='denied'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_customer/<int:id>/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('call/<int:id>/', views.call, name='call'),
    ]
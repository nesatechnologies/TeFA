from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('conformed/', views.conformed, name='conformed'),
    path('need_following/', views.need_following, name='need_following'),
    path('denied/', views.denied, name='denied'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_customer/<int:id>/', views.delete, name='delete'),
    ]
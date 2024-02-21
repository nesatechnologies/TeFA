from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('conformed/', views.conformed, name='conformed'),
    path('need_following/', views.need_following, name='need_following'),
    path('denied/', views.denied, name='denied'),
    path('users/', views.users, name='users'),

    ]
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')
def conformed(request):
    return render(request, 'conformed.html')
def need_following(request):
    return render(request, 'need_following.html')
def denied(request):
    return render(request, 'denied.html')
def users(request):
    return render(request, 'users.html')

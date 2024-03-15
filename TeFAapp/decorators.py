from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def session_login_required(view_func):
    """
    Decorator to ensure that the user is logged in via session before accessing the view.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'uid' in request.session:
            print("#################################################")
            # User is logged in via session, call the original view function
            return view_func(request, *args, **kwargs)
        else:
            # User is not logged in, redirect to the login page
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            return redirect(reverse('login'))  # Assuming your login URL name is 'login'
    return wrapper
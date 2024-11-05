from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_page')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:  
            login(request, user)
            return redirect('admin_page')
        else:
            messages.error(request, 'Invalid details or you are not an admin.')
    return render(request, 'admin_login.html')

@login_required(login_url='admin_login')
@never_cache
def admin_page(request):
    # Check if the logged-in user is a superuser

    if request.user.is_superuser:
        return render(request, 'admin_homepage.html')
    else:
        # Redirect to admin login page if the user is not a superuser
        return redirect('admin_login')

@login_required(login_url='admin_login')
@never_cache
def admin_logout(request):
    # django's logout fuction automatically delete the session
    logout(request)
    # Redirect to login after logout
    return redirect('admin_login')

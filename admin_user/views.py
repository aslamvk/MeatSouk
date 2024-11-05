from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@login_required(login_url='admin_login')
@never_cache
def user_page(request):
    query = request.GET.get('search', None)  # Handle None case if 'search' param doesn't exist
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    else:
        users = User.objects.all()  # When no query, fetch all users

    if not users.exists() and query:  # Only show 'No users found' when there's a query
        return render(request, 'admin_user_page.html', {'users': [], 'error_message': 'No users found matching the search criteria.'})

    return render(request, 'admin_user_page.html', {'users': users})


# Block a user
@login_required(login_url='admin_login')
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    user.save()
    return redirect('user_page')

# Unblock a user
@login_required(login_url='admin_login')
def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.is_active:
        user.is_active = True
    user.save()
    return redirect('user_page')
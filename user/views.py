from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
import re
from django.contrib import messages

# Create your views here.


def my_profile(request,id):
    user = get_object_or_404(User,id=id)

    return render(request, 'user/profile.html',{'user':user})

def profile_update(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form_data = {
            'username': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password')
        }

        errors = {}

        if not re.match(r'^[A-Za-z]+$', form_data['first_name']):
            errors['first_name'] = 'First name can only contain letters.'

        if not re.match(r'^[A-Za-z]+$', form_data['last_name']):
            errors['last_name'] = 'Last name can only contain letters.'

        if not re.match(r'^[A-Za-z0-9_]+$', form_data['username']):
            errors['username'] = 'Username can only contain letters, numbers, and underscores.'

        else:
            if User.objects.filter(username=form_data['username']).exclude(id=user.id).exists():
                errors['username'] = 'This username is already taken. Please choose another one.'

        if form_data['password'] and len(form_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'

        if errors:
            for field, error_message in errors.items():
                messages.error(request, f"{field.capitalize()}: {error_message}")
            return redirect('profile_update', id=id)

        user.username = form_data['username']
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']

        if form_data['password']:
            user.set_password(form_data['password'])

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('myprofile', id=id)

    return render(request, 'user/user_profile_update.html', {'user': user})

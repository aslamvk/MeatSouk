from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.


def my_profile(request,id):
    user = get_object_or_404(User,id=id)

    return render(request, 'user/profile.html',{'user':user})

def profile_update(request, id):
    user = get_object_or_404(User,id=id)
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        user.username = username
        user.email = email
        if new_password:
            user.set_password(new_password)

        user.save()
        return redirect('myprofile',id=id)
    return render(request, 'user/user_profile_update.html',{'user':user})

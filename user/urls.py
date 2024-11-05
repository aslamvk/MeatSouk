from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/<int:id>', views.my_profile, name='myprofile'),
    path('profile_update/<int:id>', views.profile_update, name='profile_update')
]
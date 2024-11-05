from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_page, name='user_page'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
]
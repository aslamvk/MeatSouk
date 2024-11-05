from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_category, name='admin_category'),
    path('add_category/', views.add_admin_category, name='add_admin_category'),
    path('edit_category/<int:category_id>/', views.edit_admin_category, name='edit_admin_category'),
    path('list_category/<int:category_id>/', views.list_category, name='list_category'),
    path('unlist_category/<int:category_id>/', views.unlist_category, name='unlist_category'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_pincode, name='admin_pincode'),
    path('add_pincode/', views.add_admin_pincode, name='add_admin_pincode'),
    path('list_pincode/<int:pincode_id>/', views.list_pincode, name='list_pincode'),
    path('unlist_pincode/<int:pincode_id>/', views.unlist_pincode, name='unlist_pincode'),
    path('selected_pincode/', views.selected_pincode, name='selected_pincode'),
]

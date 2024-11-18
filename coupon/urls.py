from django.urls import path
from . import views

urlpatterns = [
    path('admin_coupon/', views.admin_coupon, name='coupon'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
]

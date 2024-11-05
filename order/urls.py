from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.place_order, name='checkout'),
    path('add_addresses_in_checkout/', views.add_address_in_checkout, name='add_address_in_checkout'),
    path('user_single_order_items/<int:order_id>/', views.user_single_order_items, name='user_single_order_items'),
    path('user_order_details/<int:item_id>/', views.user_order_details, name='user_order_details'),
    path('user_singleitem_cancel/<int:order_item_id>/', views.user_singleitem_cancel, name='user_singleitem_cancel'),
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('admin_single_order_details/<int:id>/', views.admin_single_order_details, name='admin_single_order_details'),
    path('update_order_status/<int:id>', views.update_order_status, name='update_order_status'),
    path('user_order/', views.user_order, name='user_order'),
]
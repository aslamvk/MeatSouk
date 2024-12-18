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
    path('razorpay_payment/', views.razorpay_payment, name='razorpay_payment'),
    path('retry_payment/<int:order_id>/', views.retry_payment, name='retry_payment'),
    path('handle_payment/', views.handle_payment, name='handle_payment'),
    path('order_success/', views.order_success, name='order_success'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    path('return-order-request/<int:order_item_id>', views.user_return_order_item, name='user_return_order_item'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('download_sales_report_pdf/', views.download_sales_report_pdf, name='download_sales_report_pdf'),
    path('download_sales_report_excel/', views.download_sales_report_excel, name='download_sales_report_excel'),
    path('download-invoice/<int:item_id>/', views.download_invoice_item, name='download_invoice_item'),
]
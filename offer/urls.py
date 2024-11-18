from django.urls import path
from . import views

urlpatterns = [
    path('product_offer/', views.admin_product_offer, name='product_offer'),
    path('delete_product_offer/<int:offer_id>/', views.delete_product_offer, name='delete_product_offer'),
    path('edit_product_offer/<int:offer_id>/', views.edit_product_offer, name='edit_product_offer'),
    path('admin_offer_management/', views.admin_offer_management, name='admin_offer_management'),
    path('category_offer/', views.admin_category_offer, name='category_offer'),
    path('delete_category_offer/<int:offer_id>/', views.delete_category_offer, name='delete_category_offer'),
    path('edit_category_offer/<int:offer_id>/', views.edit_category_offer, name='edit_category_offer'),

]

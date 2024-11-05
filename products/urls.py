from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_product_view, name='admin_product_view'),
    path('add_product/', views.admin_product_add, name='admin_product_add'),
    path('edit_product/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/', views.shop, name='shop_by_category'),
    path('single_product/<int:product_id>/', views.product_details, name='single_product'),
    path('list_product/<int:product_id>/', views.list_product, name='list_product'),
    path('unlist_product/<int:product_id>/', views.unlist_product, name='unlist_product'),
]

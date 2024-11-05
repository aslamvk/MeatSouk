from django.urls import path
from . import views

urlpatterns = [
    path('address/<int:id>', views.address, name='address'),
    path('add_address/<int:id>', views.add_address, name='add_address'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('wallet/<int:user_id>',views.wallet, name='wallet'),
]

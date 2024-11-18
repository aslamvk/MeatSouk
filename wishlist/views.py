from django.shortcuts import render, get_object_or_404, redirect
from wishlist.models import Wishlist
from products.models import Products
from django.contrib import messages

# Create your views here.

def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user/wishlist.html', {'items':items} )

def add_to_wishlist(request,product_id):
    product = get_object_or_404(Products,id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user, products=product)

    if created:
        messages.success(request, f"{product.product_name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.product_name} is already in your wishlist.")

    return redirect('wishlist')

def remove_from_wishlist(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    items = Wishlist.objects.filter(user=request.user, products=product).first()

    if items:
        items.delete()
        messages.success(request, f"{product.product_name} removed from your wishlist.")
    return redirect('wishlist')
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cart.models import Cart
from products.models import Products
from cart.models import CartItems
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 0.5)
        product = get_object_or_404(Products, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item = CartItems.objects.filter(cart=cart, products=product).first()
        if cart_item:
            return JsonResponse({
                'success': False,
                'message': 'Item already in your cart. You can update the quantity from the cart.'
            })
            
        cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
        if not created:
            cart_item.quantity += float(quantity)  
        else:
            cart_item.quantity = float(quantity)  # If it's a new item, set the quantity

        cart_item.save()

        return JsonResponse({'success': True, 'message': 'Item added to cart'})
    
    return JsonResponse({'success': False, 'message': 'User not authenticated or invalid request'})

def cart_view(request):
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart = cart.items.all()
        context = {
            'items': user_cart,
        }
    else:
        context = {
            'items': [],
        }
    return render(request, 'user/cart.html', context)

@csrf_exempt
def update_quantity(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItems, cart=cart, products_id=product_id)

        if quantity > 0:
            cart_item.quantity = float(quantity)
            cart_item.save()
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid quantity'})
    
    return JsonResponse({'success': False, 'message': 'User not authenticated or invalid request'})

def remove_cart_item(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)  
        cart_item = get_object_or_404(CartItems, cart=cart, products_id=product_id) 

        cart_item.delete() 

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'User not authenticated or invalid request'})
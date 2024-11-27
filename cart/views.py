from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from cart.models import Cart
from products.models import Products
from cart.models import CartItems
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.


def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            product = get_object_or_404(Products, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Check if item already exists in cart
            cart_item = CartItems.objects.filter(cart=cart, products=product).first()
            
            if cart_item:
                return JsonResponse({
                    'success': True,
                    'already_in_cart': True,
                    'message': 'Item already in your cart. You can update the quantity from the cart.'
                })
            else:
                # Create new cart item
                cart_item = CartItems.objects.create(
                    cart=cart,
                    products=product,
                    quantity=float(quantity)
                )
                
                # Convert to integer if product unit is piece
                if product.product_unit == 'piece':
                    cart_item.quantity = int(cart_item.quantity)
                    cart_item.save()

                return JsonResponse({
                    'success': True,
                    'already_in_cart': False,
                    'message': 'Item added to cart successfully.'
                })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'User not authenticated or invalid request.'
    })

def cart_view(request):
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart = cart.items.filter(products__is_listed=True, products__category__is_listed=True)
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
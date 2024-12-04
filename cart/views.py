from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from cart.models import Cart
from products.models import Products
from cart.models import CartItems
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
from offer.models import Product_Offers, Category_Offers
from decimal import Decimal
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

        cart_items = []
        subtotal = Decimal(0)  # Initialize subtotal as a Decimal

        for item in user_cart:
            product = item.products
            price = Decimal(product.price)  # Ensure price is Decimal

            # Check for product-specific offers
            product_offer = Product_Offers.objects.filter(
                product=product,
                valid_from__lte=datetime.now(),
                valid_to__gte=datetime.now()
            ).first()

            # Check for category-specific offers
            category_offer = Category_Offers.objects.filter(
                category=product.category,
                valid_from__lte=datetime.now(),
                valid_to__gte=datetime.now()
            ).first()

            # Apply the highest offer
            discount = Decimal(0)  # Initialize discount as a Decimal
            if product_offer and category_offer:
                discount = max(Decimal(product_offer.offer_percentage), Decimal(category_offer.offer_percentage))
            elif product_offer:
                discount = Decimal(product_offer.offer_percentage)
            elif category_offer:
                discount = Decimal(category_offer.offer_percentage)

            # Calculate the discounted price
            discounted_price = price * (Decimal(1) - (discount / Decimal(100)))
            subtotal += discounted_price * Decimal(item.quantity)  # Multiply with Decimal quantity

            cart_items.append({
                'item': item,
                'discounted_price': round(discounted_price, 2),
                'total_price': round(discounted_price * Decimal(item.quantity), 2),  # Convert quantity to Decimal
            })

        # Calculate delivery charge and total
        delivery_charge = Decimal(0) if subtotal > Decimal(500) else Decimal(40)
        total = subtotal + delivery_charge

        context = {
            'items': cart_items,
            'subtotal': round(subtotal, 2),
            'delivery_charge': round(delivery_charge, 2),
            'total': round(total, 2),
        }
    else:
        context = {
            'items': [],
            'subtotal': Decimal(0),
            'delivery_charge': Decimal(0),
            'total': Decimal(0),
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
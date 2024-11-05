from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from address.models import Address
from cart.models import Cart
from cart.models import CartItems
from decimal import Decimal
from order.models import Order, OrderItem
from django.shortcuts import get_object_or_404
from pincode.models import Pincode
from django.db import transaction
# Create your views here.


@login_required(login_url='login')
def place_order(request):
    user = request.user
    address = Address.objects.filter(user=user, is_listed=True)
    cart = Cart.objects.get(user=user)
    cart_items = CartItems.objects.filter(cart=cart)

    subtotal_price = Decimal('0.00')
    cart_items_with_subtotals = []

    for item in cart_items:
        quantity = Decimal(item.quantity)
        item_price = Decimal(item.products.price) * quantity

        subtotal_price += item_price
        cart_items_with_subtotals.append({
            'item': item,
            'item_subtotal': item_price
        })

    delivery_charge = Decimal('0.00') if subtotal_price > Decimal('500.00') else Decimal('40.00')

    total_price = subtotal_price + delivery_charge


    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        payment_type = request.POST.get('option')

        if not selected_address_id or not payment_type:
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items_with_subtotals,
                'cart': cart,
                'subtotal_price': subtotal_price,
                'delivery_charge': delivery_charge,
                'total_price': total_price,
                'error_message': 'Please select an address or payment type.'
            })

        selected_address = Address.objects.get(id=selected_address_id)

        if payment_type == 'Cash on Delivery' and total_price > Decimal('1000.00'):
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items_with_subtotals,
                'cart': cart,
                'subtotal_price': subtotal_price,
                'delivery_charge': delivery_charge,
                'total_price': total_price,
                'error_message': 'Cash on Delivery is not available for orders above ₹1000.'
            })
        
        # Transaction to ensure atomicity for stock update and order creation
        with transaction.atomic():
            # Create new order
            new_order = Order.objects.create(
                user=request.user,
                address=selected_address,
                total_price=total_price,
                payment_type=payment_type,
            )

        payment_status = 'Success'

        for item in cart_items:
            quantity = Decimal(item.quantity)
            item_price = Decimal(item.products.price) * quantity

            OrderItem.objects.create(
                order=new_order,
                product=item.products,
                quantity=quantity,
                price=item.products.price,
                subtotal_price=item_price
            )

            if payment_status == 'Success':
                item.products.stock -= quantity
                item.products.save()



        cart_items.delete()
        
        return render(request, 'user/order_success.html', {
        'selected_address': selected_address,
        'total_price': total_price,
        'payment_method': payment_type,
        'order_number': new_order.order_number,
        })
    
    return render(request, 'user/checkout.html', {
        'address': address,
        'cart_items': cart_items_with_subtotals,
        'cart': cart,
        'subtotal_price': subtotal_price,
        'delivery_charge': delivery_charge,
        'total_price': total_price,
    })

@login_required(login_url='login')
def add_address_in_checkout(request):
    
     
    if request.method == 'POST':
 
        name  =  request.POST.get("name")
        phone_number= request.POST.get("phone")
        alternative_phone = request.POST.get("alt_phone")
        pincode_value = request.POST.get("pincode")
        locality = request.POST.get("locality")
        landmark = request.POST.get("landmark")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")
        address = request.POST.get("address")
        address_type = request.POST.get("addressType")
        pincode_instance = get_object_or_404(Pincode, pincode=pincode_value)

        Address.objects.create(
            user = request.user,
            full_name =name,
            phone_number = phone_number,
            alternative_phone_number =  alternative_phone,
            pincode = pincode_instance,
            locality =  locality,
            landmark = landmark,
            district =  district,
            state = state,
            country = country,
            address = address,
            address_type = address_type
        )
        return redirect('checkout')

    return render(request, "user/checkout_add_address.html")

def user_order(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'user/user_order.html', {'orders':orders})

@login_required(login_url='login')
def user_single_order_items(request, order_id):

    order = get_object_or_404(Order, id = order_id)
    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        print("Item:", item)
    
    context = {
        'order': order,
        'order_items':order_items,
    }

    return render(request, 'user/user_single_order_items.html', context)

@login_required(login_url='login')
def user_order_details(request,item_id):
    order_items = get_object_or_404(OrderItem, id=item_id)
    order = order_items.order
    context = {
       
        'order_items': order_items,
        'order' : order
    }
    return render(request,"user/user_order_details.html",context)

def user_singleitem_cancel(request,order_item_id):
    order_item =  get_object_or_404(OrderItem,id=order_item_id)

    if order_item.status in ["Order Pending", "Order confirmed"]:
        order_item.status = "Cancelled"
        order_item.save()
        # here after the order cancelled by the user. the cancelled quantity added to the stock back.
        order_item.product.stock += order_item.quantity
        order_item.product.save()

    return redirect('user_single_order_items', order_id = order_item.order.id)

def admin_order_list(request):
    orders = Order.objects.all().order_by('created_at')
    return render(request, 'admin_order_list.html',{'orders':orders})

def admin_single_order_details(request, id):
    order = get_object_or_404(Order,id=id)
    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'admin_single_order_details.html', context)

def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        # Iterate through each order item to update status
        for item in order.items.all():
            new_status = request.POST.get(f'status_{item.id}')
            old_status = item.status
            item.status = new_status
            item.save()
            
            if new_status == "Cancelled" and old_status != "Cancelled":
                item.product.stock += item.quantity
                item.product.save()
        
        return redirect('admin_order_list')
    
    return redirect('admin_single_order_details', id=id)
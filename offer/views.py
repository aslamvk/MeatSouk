from django.shortcuts import render,redirect,get_object_or_404
from offer.models import Product_Offers
from django.contrib import messages
from offer.models import Category_Offers
from products.models import Products
from category.models import Category
from django.contrib import messages
from decimal import Decimal

# Create your views here.
def admin_offer_management(request):
    return render(request, 'admin_offer_management.html')
def admin_product_offer(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    prodcut_offer = Product_Offers.objects.all()
    products = Products.objects.all()

    print("Available Products in Database:")
    for product in products:
        print(f"ID: {product.id}, Name: {product.product_name}, Price: {product.price}")

    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        product_id = request.POST.get('product')
        offer_discount = request.POST.get('offer_discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        offer_details = request.POST.get('offer_details')

        if offer_name and products and offer_discount and valid_from and valid_to and offer_details:
            try:
                product = Products.objects.get(id=product_id)
                actual_price = product.price
                max_allowed_discount = actual_price * Decimal('0.8')

                if Decimal(offer_discount) > max_allowed_discount:
                    messages.error(
                        request, 
                        f"Offer discount cannot exceed 80% of the product's price. "
                        f"Maximum allowed discount for {product.product_name} is {max_allowed_discount:.2f}."
                    )
                else:    
                    Product_Offers.objects.create(
                        offer_name = offer_name,
                        product = product,
                        offer_discount = Decimal(offer_discount),
                        valid_from = valid_from,
                        valid_to = valid_to,
                        offer_details = offer_details
                    )
                    messages.success(request, 'Product offer created successfully!')
                    return redirect('product_offer')
            except Exception as e:
                messages.error(request, f"Error creating product offer: {e}")
        else:
            messages.error(request, "Please give all the data.")
    return render(request, 'admin_product_offer.html', {'prodcut_offer': prodcut_offer, 'products': products})

def delete_product_offer(request,offer_id):
    prodcut_offer = get_object_or_404(Product_Offers,id=offer_id)
    prodcut_offer.delete()
    messages.success(request, 'Product offer deleted successfully!')
    return redirect('product_offer')

def edit_product_offer(request,offer_id):
    prodcut_offer = get_object_or_404(Product_Offers, id=offer_id)
    products = Products.objects.all()

    if request.method == 'POST':
        prodcut_offer.offer_name = request.POST.get('offer_name')
        product_id = request.POST.get('product')
        prodcut_offer.product = get_object_or_404(Products, id=product_id)
        prodcut_offer.offer_discount = request.POST.get('offer_discount')
        prodcut_offer.valid_from = request.POST.get('valid_from')
        prodcut_offer.valid_to = request.POST.get('valid_to')
        prodcut_offer.offer_details = request.POST.get('offer_details')

        prodcut_offer.save()
        
        messages.success(request,"product offer Successfully edited")
        return redirect('product_offer')
    return render(request, 'admin_product_offer_edit.html', {'prodcut_offer': prodcut_offer, 'products': products})

def admin_category_offer(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    category_offer = Category_Offers.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        category_id = request.POST.get('category')
        offer_discount = request.POST.get('offer_discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        offer_details = request.POST.get('offer_details')

        if offer_name and categories and offer_discount and valid_from and valid_to and offer_details:
            try:
                category = Category.objects.get(id=category_id)
                Category_Offers.objects.create(
                    offer_name = offer_name,
                    category = category,
                    offer_discount = offer_discount,
                    valid_from = valid_from,
                    valid_to = valid_to,
                    offer_details = offer_details
                )
                messages.success(request, 'category offer created successfully!')
                return redirect('category_offer')
            except Exception as e:
                messages.error(request, f"Error creating category offer: {e}")
        else:
            messages.error(request, "Please give all the data.")
    return render(request, 'admin_category_offer.html', {'category_offer': category_offer, 'categories':categories})

def delete_category_offer(request,offer_id):
    category_offer = get_object_or_404(Category_Offers,id=offer_id)
    category_offer.delete()
    messages.success(request, 'category offer deleted successfully!')
    return redirect('category_offer')

def edit_category_offer(request,offer_id):
    category_offer = get_object_or_404(Category_Offers, id=offer_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_offer.offer_name = request.POST.get('offer_name')
        category_id = request.POST.get('category')
        category_offer.category = get_object_or_404(Category, id=category_id)
        category_offer.offer_discount = request.POST.get('offer_discount')
        category_offer.valid_from = request.POST.get('valid_from')
        category_offer.valid_to = request.POST.get('valid_to')
        category_offer.offer_details = request.POST.get('offer_details')

        category_offer.save()
        
        messages.success(request,"category offer Successfully edited")
        return redirect('category_offer')
    return render(request, 'admin_category_offer_edit.html', {'category_offer': category_offer, 'categories': categories,})
from django.shortcuts import render,redirect,get_object_or_404
from offer.models import Product_Offers
from django.contrib import messages
from offer.models import Category_Offers
from products.models import Products
from category.models import Category
from django.contrib import messages
from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='admin_login')
@never_cache
def admin_offer_management(request):
    return render(request, 'admin_offer_management.html')

@login_required(login_url='admin_login')
@never_cache
def admin_product_offer(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    product_offer = Product_Offers.objects.all()
    products = Products.objects.all()

    print("Available Products in Database:")
    for product in products:
        print(f"ID: {product.id}, Name: {product.product_name}, Price: {product.price}")

    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        product_id = request.POST.get('product')
        offer_percentage = request.POST.get('offer_percentage')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        offer_details = request.POST.get('offer_details')

        if offer_name and products and offer_percentage and valid_from and valid_to and offer_details:
            try:
                offer_percentage = Decimal(offer_percentage)
                if offer_percentage > 80:
                    messages.error(
                        request,
                        "Discount percentage cannot exceed 80%."
                    )
                else:
                    product = Products.objects.get(id=product_id)
                    Product_Offers.objects.create(
                        offer_name=offer_name,
                        product=product,
                        offer_percentage=offer_percentage,
                        valid_from=valid_from,
                        valid_to=valid_to,
                        offer_details=offer_details
                    )
                    messages.success(request, 'Product offer created successfully!')
                    return redirect('product_offer')
            except Exception as e:
                messages.error(request, f"Error creating product offer: {e}")
        else:
            messages.error(request, "Please provide all the required data.")
    return render(request, 'admin_product_offer.html', {'product_offer': product_offer, 'products': products})

def delete_product_offer(request,offer_id):
    prodcut_offer = get_object_or_404(Product_Offers,id=offer_id)
    prodcut_offer.delete()
    messages.success(request, 'Product offer deleted successfully!')
    return redirect('product_offer')

@login_required(login_url='admin_login')
@never_cache
def edit_product_offer(request, offer_id):
    product_offer = get_object_or_404(Product_Offers, id=offer_id)
    products = Products.objects.all()

    if request.method == 'POST':
        product_offer.offer_name = request.POST.get('offer_name')
        product_id = request.POST.get('product')
        product_offer.product = get_object_or_404(Products, id=product_id)
        offer_percentage = Decimal(request.POST.get('offer_percentage'))
        
        if offer_percentage > 80:
            messages.error(
                request,
                "Offer percentage cannot exceed 80%."
            )
        else:
            product_offer.offer_percentage = offer_percentage
            product_offer.valid_from = request.POST.get('valid_from')
            product_offer.valid_to = request.POST.get('valid_to')
            product_offer.offer_details = request.POST.get('offer_details')
            product_offer.save()
            messages.success(request, "Product offer successfully edited")
            return redirect('product_offer')

    return render(request, 'admin_product_offer_edit.html', {'product_offer': product_offer, 'products': products})

@login_required(login_url='admin_login')
@never_cache
def admin_category_offer(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    category_offer = Category_Offers.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        category_id = request.POST.get('category')
        offer_percentage = request.POST.get('offer_percentage')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        offer_details = request.POST.get('offer_details')

        if offer_name and category_id and offer_percentage and valid_from and valid_to and offer_details:
            try:
                offer_percentage = Decimal(offer_percentage)
                if offer_percentage > 80:
                    messages.error(
                        request,
                        "Offer percentage cannot exceed 80%."
                    )
                else:
                    category = Category.objects.get(id=category_id)
                    Category_Offers.objects.create(
                        offer_name=offer_name,
                        category=category,
                        offer_percentage=offer_percentage,
                        valid_from=valid_from,
                        valid_to=valid_to,
                        offer_details=offer_details
                    )
                    messages.success(request, 'Category offer created successfully!')
                    return redirect('category_offer')
            except Exception as e:
                messages.error(request, f"Error creating category offer: {e}")
        else:
            messages.error(request, "Please provide all the required data.")
    return render(request, 'admin_category_offer.html', {'category_offer': category_offer, 'categories': categories})

def delete_category_offer(request,offer_id):
    category_offer = get_object_or_404(Category_Offers,id=offer_id)
    category_offer.delete()
    messages.success(request, 'category offer deleted successfully!')
    return redirect('category_offer')

@login_required(login_url='admin_login')
@never_cache
def edit_category_offer(request,offer_id):
    category_offer = get_object_or_404(Category_Offers, id=offer_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_offer.offer_name = request.POST.get('offer_name')
        category_id = request.POST.get('category')
        category_offer.category = get_object_or_404(Category, id=category_id)
        offer_percentage = Decimal(request.POST.get('offer_percentage'))

        if offer_percentage > 80:
            messages.error(
                request,
                "Offer percentage cannot exceed 80%."
            )
        else:
            category_offer.offer_percentage = offer_percentage
            category_offer.valid_from = request.POST.get('valid_from')
            category_offer.valid_to = request.POST.get('valid_to')
            category_offer.offer_details = request.POST.get('offer_details')
            category_offer.save()
            messages.success(request, "Category offer successfully edited")
            return redirect('category_offer')

    return render(request, 'admin_category_offer_edit.html', {'category_offer': category_offer, 'categories': categories})
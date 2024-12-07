from django.shortcuts import render,redirect,get_object_or_404
from products.models import Products
from category.models import Category
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache
from pincode.models import Pincode
from offer.models import Product_Offers, Category_Offers
from datetime import datetime
from django.http import JsonResponse
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required(login_url='admin_login')
@never_cache
def admin_product_view(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        products = Products.objects.filter(
            Q(id__icontains=search_query) |
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query)
        )
    else:
        products = Products.objects.all()

    paginator = Paginator(products, 10)
    page = request.GET.get('page', 1)
    
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
        

    return render(request, 'admin_product_view.html', {'products': paginated_products})

@login_required(login_url='admin_login')
@never_cache
def admin_product_add(request):
    categories = Category.objects.all()
    pincodes = Pincode.objects.all()
    error_message = None

    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_unit = request.POST.get('product_unit')
        product_description = request.POST.get('product_description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        selected_pincodes = request.POST.getlist('pincodes')

        if not product_name:
            error_message = "Product name is required and cannot be blank."
        elif not category_id or not price or not stock or not product_unit or not product_description:
            error_message = "All fields are required."
        elif Decimal(price) <= Decimal('0'):
            error_message = "Price must be greater than zero."
        elif not image1 or not image2 or not image3:
            error_message = "All three product images are required."
        else:
            try:
                if product_unit == 'kg':
                    try:
                        stock_decimal = Decimal(stock)
                        if stock_decimal <= Decimal('0'):
                            error_message = "Stock must be greater than zero."
                        elif stock_decimal < Decimal('0.01'):
                            error_message = "Minimum stock for kg products should be 0.01 kg"
                    except (ValueError, TypeError):
                        error_message = "Invalid stock value for kg unit"
                
                elif product_unit == 'piece':
                    try:
                        stock_decimal = Decimal(stock)
                        if stock_decimal % 1 != 0:
                            error_message = "Stock must be a whole number for piece units (no fractions allowed)"
                        elif stock_decimal <= Decimal('0'):
                            error_message = "Stock must be greater than zero."
                        stock_decimal = int(stock_decimal)
                    except (ValueError, TypeError):
                        error_message = "Stock must be a whole number for piece units"
                
                else:
                    error_message = "Invalid unit type. Must be either 'kg' or 'piece'"

                if not error_message:
                    if Products.objects.filter(product_name__iexact=product_name, product_unit=product_unit).exists():
                        error_message = f"A product variant with the name '{product_name}' and unit '{product_unit}' already exists."
                    else:
                        category = Category.objects.get(id=category_id)
                        product = Products(
                            product_name=product_name,
                            category=category,
                            price=Decimal(price),
                            stock=stock_decimal,
                            product_unit=product_unit,
                            product_description=product_description,
                            image1=image1,
                            image2=image2,
                            image3=image3
                        )
                        product.save()

                        product.pincode.set(selected_pincodes)

                        return redirect('admin_product_view')

            except ValidationError as e:
                error_message = str(e)

    context = {
        'categories': categories,
        'pincodes': pincodes,
        'error_message': error_message,
        'unit_choices': Products.UNIT_CHOICES,
    }
    return render(request, 'admin_product_add.html', context)

@login_required(login_url='admin_login')
@never_cache
def admin_product_edit(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    categories = Category.objects.all()
    product_pincodes = product.pincode.values_list('id', flat=True)
    pincodes = Pincode.objects.all()
    error_message = None

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            selected_pincodes = request.POST.getlist('pincodes')
            product.pincode.clear()
            if selected_pincodes:
                pincodes = Pincode.objects.filter(id__in=selected_pincodes)
                product.pincode.add(*pincodes)
            product.save()
            return JsonResponse({
                'status': 'success', 
                'message': 'Pincodes updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=400)

    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_unit = request.POST.get('product_unit')
        product_description = request.POST.get('product_description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        selected_pincodes = request.POST.getlist('pincodes') or list(product_pincodes)

        if not product_name:
            error_message = "Product name is required and cannot be blank."
        elif not category_id or not price or not stock or not product_unit or not product_description:
            error_message = "All fields are required."
        elif Decimal(price) <= Decimal('0'):
            error_message = "Price must be greater than zero."
        else:
            try:
                if product_unit == 'piece':
                    try:
                        stock_decimal = Decimal(stock)
                        if stock_decimal % 1 != 0:
                            error_message = "Stock must be a whole number for piece units (no fractions allowed)"
                        elif stock_decimal <= Decimal('0'):
                            error_message = "Stock must be greater than zero."
                        stock_decimal = int(stock_decimal)
                    except (ValueError, TypeError):
                        error_message = "Stock must be a whole number for piece units"
                elif product_unit == 'kg':
                    try:
                        stock_decimal = Decimal(stock)
                        if stock_decimal <= Decimal('0'):
                            error_message = "Stock must be greater than zero."
                        elif stock_decimal < Decimal('0.01'):
                            error_message = "Minimum stock for kg products should be 0.01 kg"
                    except (ValueError, TypeError):
                        error_message = "Invalid stock value for kg unit"

                if not error_message:
                    duplicate_exists = Products.objects.filter(
                        product_name__iexact=product_name,
                        product_unit=product_unit
                    ).exclude(id=product_id).exists()
                    
                    if duplicate_exists:
                        error_message = f"A product variant with the name '{product_name}' and unit '{product_unit}' already exists."
                    else:
                        category = Category.objects.get(id=category_id)
                        product.product_name = product_name
                        product.category = category
                        product.price = Decimal(price)
                        product.stock = stock_decimal
                        product.product_unit = product_unit
                        product.product_description = product_description

                        if image1:
                            product.image1 = image1
                        if image2:
                            product.image2 = image2
                        if image3:
                            product.image3 = image3

                        product.save()

                        product.pincode.clear()
                        if selected_pincodes:
                            pincodes = Pincode.objects.filter(id__in=selected_pincodes)
                            product.pincode.add(*pincodes)

                        return redirect('admin_product_view')

            except ValidationError as e:
                error_message = str(e)

    context = {
        'product': product,
        'categories': categories,
        'pincodes': pincodes,
        'product_pincodes': product_pincodes,
        'error_message': error_message,
        'unit_choices': Products.UNIT_CHOICES,
    }
    return render(request, 'admin_product_edit.html', context)

@login_required(login_url='login')
@never_cache
def shop(request):
    categories = Category.objects.filter(is_listed=True)
    selected_category = request.GET.get('category', 'All')
    search_query = request.GET.get('query', None)
    sort_option = request.GET.get('sort', None)
    cities = Pincode.objects.filter(is_listed=True).values_list('city', flat=True).distinct()
    selected_city = request.GET.get('city')

    pincode = request.session.get('pincode')
    city = request.session.get('city')

    if selected_city:
        request.session['city'] = selected_city
        request.session['pincode'] = None
        city = selected_city

    if selected_category == 'All':
        products = Products.objects.filter(category__is_listed=True, is_listed=True)
    else:
        products = Products.objects.filter(category__category_name=selected_category, is_listed=True)
    
    error_message = None
    
    if pincode:
        try:
            pincode_obj = Pincode.objects.get(pincode=pincode, is_listed=True)
            products = products.filter(pincode__city=pincode_obj.city)
        except Pincode.DoesNotExist:
            error_message = "Products are not available for this pincode. Please enter another pincode or select a different location."
            products = products.none()
    elif city:
        products = products.filter(pincode__city=city)

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query) |
            Q(product_description__icontains=search_query)
        )

    if not products.exists() and search_query:
        error_message = f"No products found for '{search_query}'"

    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'name_asc':
        products = products.order_by('product_name')
    elif sort_option == 'name_desc':
        products = products.order_by('-product_name')

    now = datetime.now()
    products_with_offers = []

    for product in products:
        product_offer = Product_Offers.objects.filter(
            product=product, valid_from__lte=now, valid_to__gte=now
        ).first()
        category_offer = Category_Offers.objects.filter(
            category=product.category, valid_from__lte=now, valid_to__gte=now
        ).first()

        product_discount_percentage = product_offer.offer_percentage if product_offer else 0
        category_discount_percentage = category_offer.offer_percentage if category_offer else 0

        best_offer = None
        final_price = product.price
        discount_percentage = 0
        if product_discount_percentage > category_discount_percentage:
            best_offer = product_offer
            discount_percentage = product_discount_percentage
        elif category_discount_percentage > 0:
            best_offer = category_offer
            discount_percentage = category_discount_percentage

        final_price -= (final_price * discount_percentage / 100)

        products_with_offers.append({
            'product': product,
            'best_offer': best_offer,
            'final_price': round(final_price, 2),
            'discount_percentage': round(discount_percentage, 2),
        })

    paginator = Paginator(products_with_offers, 12)
    page = request.GET.get('page', 1)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'products': paginated_products,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_option': sort_option,
        'error_message': error_message,
        'cities': cities,
        'current_city': city,
    }
    return render(request, 'user/shop.html', context)



@login_required(login_url='login')
@never_cache
def product_details(request,product_id):
    product = get_object_or_404(Products,id=product_id)
    username = request.user.username

    now = datetime.now()
    product_offer = Product_Offers.objects.filter(
        product=product, valid_from__lte=now, valid_to__gte=now
    ).first()
    category_offer = Category_Offers.objects.filter(
        category=product.category, valid_from__lte=now, valid_to__gte=now
    ).first()
    product_discount = product_offer.offer_percentage if product_offer else 0
    category_discount = category_offer.offer_percentage if category_offer else 0

    best_offer = None
    final_price = product.price
    discount_percentage = 0

    if product_discount > category_discount:
        best_offer = product_offer
        discount_amount = (product.price * product_discount) / 100
        final_price = product.price - discount_amount
        discount_percentage = product_discount
    elif category_discount > 0:
        best_offer = category_offer
        discount_amount = (product.price * category_discount) / 100
        final_price = product.price - discount_amount
        discount_percentage = category_discount

    context = {
        'product': product,
        'best_offer': best_offer,
        'final_price': round(final_price, 2),
        'username': username,
        'discount_percentage': round(discount_percentage, 2),
    }
    return render(request, 'user/product-single.html', context)

def unlist_product(request, product_id):
    user = Products.objects.get(id=product_id)
    if user.is_listed:
        user.is_listed = False
    user.save()
    return redirect('admin_product_view')

def list_product(request, product_id):
    user = Products.objects.get(id=product_id)
    if not user.is_listed:
        user.is_listed = True
    user.save()
    return redirect('admin_product_view')
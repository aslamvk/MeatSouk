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
# Create your views here.

@login_required(login_url='admin_login')
@never_cache
def admin_product_view(request):
    # Fetch the search query from the request
    search_query = request.GET.get('search_query', '')

    # If there is a search query, filter the products accordingly
    if search_query:
        products = Products.objects.filter(
            Q(id__icontains=search_query) |
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query)
        )
    else:
        products = Products.objects.all()  # Retrieve all products when no search query is provided
        

    return render(request, 'admin_product_view.html', {'products': products})

@login_required(login_url='admin_login')
@never_cache
def admin_product_add(request):
    categories = Category.objects.all()  # Fetch all categories
    pincodes = Pincode.objects.all()  # Fetch all available pincodes
    error_message = None

    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()  # Remove leading/trailing whitespace
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_description = request.POST.get('product_description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        selected_pincodes = request.POST.getlist('pincodes')

        # Validation
        if not product_name:
            error_message = "Product name is required and cannot be blank."
        elif not category_id or not price or not stock or not product_description:
            error_message = "All fields are required."
        elif float(price) <= 0:
            error_message = "Price must be greater than zero."
        elif int(stock) <= 0:
            error_message = "Stock must be greater than zero."
        elif not image1 or not image2 or not image3:
            error_message = "All three product images are required."
        else:
            try:
                # Check if a product with the same name already exists
                if Products.objects.filter(product_name__iexact=product_name).exists():
                    error_message = "A product with this name already exists."
                else:
                    # Proceed with saving the product
                    category = Category.objects.get(id=category_id)
                    product = Products(
                        product_name=product_name,
                        category=category,
                        price=price,
                        stock=stock,
                        product_description=product_description,
                        image1=image1,
                        image2=image2,
                        image3=image3
                    )
                    product.save()

                    # Save selected pincodes to product
                    product.pincode.set(selected_pincodes)

                return redirect('admin_product_view')
            except ValidationError as e:
                error_message = str(e)

    context = {
        'categories': categories,
        'pincodes': pincodes,
        'error_message': error_message
    }
    return render(request, 'admin_product_add.html', context)

@login_required(login_url='admin_login')
@never_cache
def admin_product_edit(request, product_id):
    product = get_object_or_404(Products, id=product_id)  # Get the product by ID
    categories = Category.objects.all()
    product_pincodes = product.pincode.values_list('id', flat=True)
    pincodes = Pincode.objects.all()
    error_message = None

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_description = request.POST.get('product_description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        selected_pincodes = request.POST.getlist('pincodes')

        # Validation
        if not product_name or not category_id or not price or not stock or not product_description:
            error_message = "All fields are required."
        elif '*' in product_name or '*' in product_description:
            error_message = "Product name and description cannot contain the '*' character."
        elif float(price) <= 0:
            error_message = "Price must be greater than zero."
        elif int(stock) <= 0:
            error_message = "Stock must be greater than zero."
        else:
            try:
                category = Category.objects.get(id=category_id)
                product.product_name = product_name
                product.category = category
                product.price = price
                product.stock = stock
                product.product_description = product_description

                # Update product images if new ones are uploaded
                if image1:
                    product.image1 = image1
                if image2:
                    product.image2 = image2
                if image3:
                    product.image3 = image3

                product.save()
                product.pincode.set(selected_pincodes)
                return redirect('admin_product_view')  # Redirect after successful product edit
            except Exception as e:
                error_message = str(e)

    context = {
        'product': product,
        'categories': categories,
        'pincodes': pincodes,
        'product_pincodes': product_pincodes,
        'error_message': error_message
    }
    return render(request, 'admin_product_edit.html', context)

@login_required(login_url='login')
@never_cache
def shop(request):
    # Get all categories
    categories = Category.objects.filter(is_listed=True)
    
    # Get selected category from the query parameters, default to 'All'
    selected_category = request.GET.get('category', 'All')

    # searched query from the search place
    search_query = request.GET.get('query', None)

    # taking the sort
    sort_option = request.GET.get('sort', None)

    # Filter products based on the selected category
    if selected_category == 'All':
        products = Products.objects.filter(category__is_listed=True, is_listed=True)
    else:
        products = Products.objects.filter(category__category_name=selected_category, is_listed=True)
    
    # Retrieve pincode or city from session
    pincode = request.session.get('pincode')
    city = request.session.get('city')
    error_message = None

    # Filter products based on session data
    if pincode:
        # Filter by pincode if it exists in session
        try:
            pincode_obj = Pincode.objects.get(pincode=pincode, is_listed=True)
            products = products.filter(pincode__city=pincode_obj.city)
        except Pincode.DoesNotExist:
            error_message = "Products are not available for this pincode. Please enter another pincode or select a different location."
            products = products.none()
    elif city:
        # Filter by city if pincode is not set but city is
        products = products.filter(pincode__city=city)

    # Filter products based on search query
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query) |
            Q(product_description__icontains=search_query)
        )

    if not products.exists() and search_query:
        error_message = f"No products found for '{search_query}'"

        # sorting application for products
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
        # Get product-specific and category-specific offers
        product_offer = Product_Offers.objects.filter(
            product=product, valid_from__lte=now, valid_to__gte=now
        ).first()
        category_offer = Category_Offers.objects.filter(
            category=product.category, valid_from__lte=now, valid_to__gte=now
        ).first()

        product_discount = (
            (product_offer.offer_discount / product.price) * 100 if product_offer else 0
        )
        category_discount = (
            (category_offer.offer_discount / product.price) * 100 if category_offer else 0
        )

        # Determine the best offer
        best_offer = None
        final_price = product.price
        discount_percentage = 0
        if product_discount > category_discount:
            best_offer = product_offer
            final_price = product.price - product_offer.offer_discount
            discount_percentage = product_discount
        elif category_discount > 0:
            best_offer = category_offer
            final_price = product.price - category_offer.offer_discount
            discount_percentage = category_discount

        products_with_offers.append({
            'product': product,
            'best_offer': best_offer,
            'final_price': final_price,
            'discount_percentage': round(discount_percentage, 2),
        })

    context = {
        'categories': categories,
        'products': products_with_offers,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_option': sort_option,
        'error_message': error_message,
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
    product_discount = (
        (product_offer.offer_discount / product.price) * 100 if product_offer else 0
    )
    category_discount = (
        (category_offer.offer_discount / product.price) * 100 if category_offer else 0
    )

    best_offer = None
    final_price = product.price
    discount_percentage = 0
    if product_discount > category_discount:
        best_offer = product_offer
        final_price = product.price - product_offer.offer_discount
        discount_percentage = product_discount
    elif category_discount > 0:
        best_offer = category_offer
        final_price = product.price - category_offer.offer_discount
        discount_percentage = category_discount

    context = {
        'product': product,
        'best_offer': best_offer,
        'final_price': final_price,
        'username': username,
        'discount_percentage': round(discount_percentage, 2),
    }
    return render(request,'user/product-single.html', context)

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
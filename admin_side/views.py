from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from datetime import datetime, timedelta
from order.models import Order, OrderItem
from products.models import Products
from django.db.models import Sum, F, Value, DecimalField, Q, Func, DateTimeField
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models.functions import Coalesce

# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_page')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:  
            login(request, user)
            return redirect('admin_page')
        else:
            messages.error(request, 'Invalid details or you are not an admin.')
    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
@never_cache
def admin_page(request):
    if request.user.is_superuser:
        total_users = User.objects.filter(is_superuser=False).count()
        total_products = Products.objects.count()
        
        orders = Order.objects.all()
        total_revenue = (orders.annotate(total_discount=Coalesce(F('coupon_discount'), Value(0, output_field=DecimalField())) + Coalesce(F('offer_discount'), Value(0, output_field=DecimalField())),
                                        valid_sales_price=Coalesce(F('total_price'), Value(0, output_field=DecimalField())) - Coalesce(F('coupon_discount'), Value(0, output_field=DecimalField())) - Coalesce(F('offer_discount'), Value(0, output_field=DecimalField()))
                        )
                        .filter(~Q(items__status__in=['Cancelled', 'Approve Return'])
                        )
                        .aggregate(total_revenue=Coalesce(Sum('valid_sales_price'),Value(0, output_field=DecimalField())
                                    )
                        )
                        )['total_revenue']
        
        total_orders = orders.count()
        
        total_units = OrderItem.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        overall_order_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or Decimal('0.00')
        
        total_discount = orders.aggregate(
            total_discount=Sum('offer_discount') + Sum('coupon_discount')
        )['total_discount'] or Decimal('0.00')
        
        cancelled_orders = OrderItem.objects.filter(status='Cancelled').count()
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        daily_sales = Order.objects.filter(
            created_at__gte=thirty_days_ago
        ).annotate(
            day=TruncDay('created_at')
        ).values('day').annotate(
            total_sales=Sum('total_price')
        ).order_by('day')

        chart_labels = [sale['day'].strftime('%Y-%m-%d') for sale in daily_sales]
        chart_values = [float(sale['total_sales']) for sale in daily_sales]

        top_selling_products = (
            OrderItem.objects.values(
                'product', 'product__product_name', 'product__price', 'product__image1', 'product__product_unit'
            )
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:6]
        )

        top_selling_categories = OrderItem.objects.values(
            'product__category__id', 
            'product__category__category_name'
        ).annotate(
            total_category_sold=Sum('quantity'),
            total_category_revenue=Sum(F('quantity') * F('product__price'))
        ).order_by('-total_category_sold')[:2]

        context = {
            'total_users': total_users,
            'total_products': total_products,
            'total_revenue': total_revenue,
            'total_units': total_units,
            'total_orders': total_orders,
            'overall_order_amount': overall_order_amount,
            'total_discount': total_discount,
            'cancelled_orders': cancelled_orders,
            'chart_labels': chart_labels,
            'chart_values': chart_values,
            'top_selling_products': top_selling_products,
            'top_selling_categories': top_selling_categories,
        }

        return render(request, 'admin_homepage.html', context)
    else:
        return redirect('admin_login')
    
def get_sales_data(request):
    time_range = request.GET.get('time_range', 'day')

    if time_range == 'day':
        days_ago = 30
        trunc_func = TruncDay
        date_format = '%Y-%m-%d'
    elif time_range == 'week':
        days_ago = 90
        trunc_func = TruncWeek
        date_format = '%Y-%W'
    elif time_range == 'month':
        days_ago = 365
        trunc_func = TruncMonth
        date_format = '%Y-%m'
    elif time_range == 'year':
        days_ago = 365 * 5
        trunc_func = TruncYear
        date_format = '%Y'
    else:
        days_ago = 30
        trunc_func = TruncDay
        date_format = '%Y-%m-%d'

    start_date = datetime.now() - timedelta(days=days_ago)

    sales_data = Order.objects.filter(
        created_at__gte=start_date
    ).annotate(
        period=trunc_func('created_at')
    ).values('period').annotate(
        total_sales=Sum('total_price')
    ).order_by('period')

    labels = [item['period'].strftime(date_format) for item in sales_data]
    values = [float(item['total_sales']) for item in sales_data]

    return JsonResponse({
        'labels': labels,
        'values': values
    })

@login_required(login_url='admin_login')
@never_cache
def admin_logout(request):
    # django's logout fuction automatically delete the session
    logout(request)
    # Redirect to login after logout
    return redirect('admin_login')

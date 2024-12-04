from django.shortcuts import render, redirect, get_object_or_404
from coupon.models import Coupon
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='admin_login')
@never_cache
def admin_coupon(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    coupon = Coupon.objects.all()

    if request.method == 'POST':
        code = request.POST.get('code')
        discount_value = request.POST.get('discount_value')
        minimum_purchase_amount = request.POST.get('minimum_purchase_amount')
        valid_from = request.POST.get('valid_from')
        valid_upto = request.POST.get('valid_upto')
        coupon_limit = request.POST.get('coupon_limit')

        try:
            discount_value = float(discount_value)
            minimum_purchase_amount = float(minimum_purchase_amount)
            
            if discount_value > (minimum_purchase_amount / 2):
                messages.error(request, "Discount value cannot exceed 50% of the minimum purchase amount.")
            elif code and discount_value and minimum_purchase_amount and valid_from and valid_upto and coupon_limit:
                try:
                    Coupon.objects.create(
                        code=code,
                        discount_value=discount_value,
                        minimum_purchase_amount=minimum_purchase_amount,
                        valid_from=valid_from,
                        valid_upto=valid_upto,
                        coupon_limit=coupon_limit
                    )
                    messages.success(request, 'Coupon created successfully!')
                    return redirect('coupon')
                except Exception as e:
                    messages.error(request, f"Error creating coupon: {e}")
            else:
                messages.error(request, "Please provide all the data.")
        except ValueError:
            messages.error(request, "Invalid discount or minimum purchase amount.")

    return render(request, 'admin_coupon.html', {'coupon': coupon})


def delete_coupon(request,coupon_id):
    coupon = get_object_or_404(Coupon,id=coupon_id)
    coupon.delete()
    messages.success(request, 'Coupon deleted successfully!')
    return redirect('coupon')

@login_required(login_url='admin_login')
@never_cache
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == 'POST':
        try:
            coupon.code = request.POST.get('code')
            discount_value = float(request.POST.get('discount_value'))
            minimum_purchase_amount = float(request.POST.get('minimum_purchase_amount'))

            if discount_value > (minimum_purchase_amount / 2):
                messages.error(request, "Discount value cannot exceed 50% of the minimum purchase amount.")
            else:
                coupon.discount_value = discount_value
                coupon.minimum_purchase_amount = minimum_purchase_amount
                coupon.valid_from = request.POST.get('valid_from')
                coupon.valid_upto = request.POST.get('valid_upto')
                coupon.coupon_limit = request.POST.get('coupon_limit')

                coupon.save()
                messages.success(request, "Coupon successfully edited!")
                return redirect('edit_coupon', coupon_id=coupon_id)
        except ValueError:
            messages.error(request, "Invalid discount or minimum purchase amount.")

    return render(request, 'admin_coupon_edit.html', {'coupon': coupon})
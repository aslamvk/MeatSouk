from django.shortcuts import render, redirect
from pincode.models import Pincode
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@login_required(login_url='admin_login')
@never_cache
def admin_pincode(request):
    pincodes = Pincode.objects.all()
    return render(request, 'admin_pincode.html', {'pincodes': pincodes})

from django.shortcuts import render, redirect
from .models import Pincode
import re  # Import regular expressions module

@login_required(login_url='admin_login')
@never_cache
def add_admin_pincode(request):
    error_message = None  # This will store any error messages

    if request.method == 'POST':
        # Retrieve data from the form
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        is_listed = request.POST.get('is_listed') == 'on'

        # Validate required fields
        if not all([pincode, city, district, state]):
            error_message = 'All fields except "Is Listed?" are required.'
        # Validate pincode: must be exactly 6 digits
        elif not re.fullmatch(r'\d{6}', pincode):
            error_message = 'Pincode must be exactly 6 digits.'
        else:
            try:
                # Create and save the new Pincode record
                new_pincode = Pincode(
                    pincode=pincode,
                    city=city,
                    district=district,
                    state=state,
                    is_listed=is_listed
                )
                new_pincode.save()
                return redirect('admin_pincode')  # Redirect on successful save
            except Exception as e:
                error_message = f'Error saving pincode: {e}'

    # Pass error_message to the template
    return render(request, 'admin_pincode_add.html', {'error_message': error_message})


def unlist_pincode(request, pincode_id):
    user = Pincode.objects.get(id=pincode_id)
    if user.is_listed:
        user.is_listed = False
    user.save()
    return redirect('admin_pincode')

def list_pincode(request, pincode_id):
    user = Pincode.objects.get(id=pincode_id)
    if not user.is_listed:
        user.is_listed = True
    user.save()
    return redirect('admin_pincode')

def selected_pincode(request):
    return render(request, 'homepage.html')
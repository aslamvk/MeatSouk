from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from address.models import Address
from pincode.models import Pincode
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def address(request, id):
    user = get_object_or_404(User, id=id)
    # to take only not deleted addresses
    addresses = user.addresses.filter(is_listed=True)
    return render(request, 'user/address_management.html', {'user': user, 'addresses': addresses})

def add_address(request, id):
    user = get_object_or_404(User, id=id)
    error_message = None

    # Retrieve the pincode from session
    session_pincode = request.session.get('pincode')

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        alt_phone = request.POST.get('alt_phone')
        pincode_value = request.POST.get('pincode')
        locality = request.POST.get('locality')
        landmark = request.POST.get('landmark')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address_text = request.POST.get('address')
        address_type = request.POST.get('addressType')

        if len(phone) != 10 or not phone.isdigit():
            error_message = 'Phone number must be exactly 10 digits.'
        elif alt_phone and (len(alt_phone) != 10 or not alt_phone.isdigit()):
            error_message = 'Alternative phone number must be exactly 10 digits.'
        elif not Pincode.objects.filter(pincode=pincode_value).exists():
            error_message = 'The products are not available in this pincode. Please try another.'

        if error_message:
            return render(request, 'user/add_address.html', {
                'user': user,
                'error_message': error_message,
                'session_pincode': session_pincode
            })

        address_type_map = {'Home': 'Home', 'Other': 'Other'}
        address_type_code = address_type_map.get(address_type)

        Address.objects.create(
            user=user,
            full_name = name,
            phone_number=phone,
            alternative_phone_number=alt_phone,
            pincode=Pincode.objects.get(pincode=pincode_value),
            locality=locality,
            landmark=landmark,
            district=district,
            state=state,
            country=country,
            address=address_text,
            address_type=address_type_code
        )
        
        return redirect('address', id=user.id)

    return render(request, 'user/add_address.html', {'user': user,'session_pincode': session_pincode})

def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id)
        
        # Only delete if the address belongs to the current user
        if request.user == address.user:
            if address.is_listed:
                address.is_listed=False
            address.save()
            return HttpResponseRedirect(f"{reverse('address', args=[request.user.id])}?status=success")
        else:
            return HttpResponseRedirect(f"{reverse('address', args=[request.user.id])}?status=failed")
        
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)  
    if request.method == 'POST':
        pincode_value = request.POST.get('pincode')

        try:
            pincode = Pincode.objects.get(pincode=pincode_value)
        except Pincode.DoesNotExist:
            return render(request, 'user/edit_address.html', {'address': address, 'error_message': 'Invalid pincode.'})
        address.full_name = request.POST.get('name')
        address.phone_number = request.POST.get('phone')
        address.alternative_phone_number = request.POST.get('alt_phone')
        address.pincode = pincode
        address.locality = request.POST.get('locality')
        address.landmark = request.POST.get('landmark')
        address.district = request.POST.get('district')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.address = request.POST.get('address')
        address.address_type= request.POST.get('addressType')
        address.save()
        
        return redirect('address', id=request.user.id)

    return render(request,'user/edit_address.html',{'address': address})
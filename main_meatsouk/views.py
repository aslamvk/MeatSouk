from django.shortcuts import render, redirect
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import re
from django.contrib.auth import login, get_user_model
from django.contrib.auth import get_user_model
from pincode.models import Pincode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# to generate six digit otp
def generate_otp():
    return random.randint(100000, 999999)

def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first-name'),
            'last_name': request.POST.get('last-name'),
            'email': request.POST.get('email'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            're_password': request.POST.get('re-enter-password')
        }
        errors = {}

        # Validate first name and last name (only letters allowed)
        if not re.match(r'^[A-Za-z]+$', form_data['first_name']):
            errors['first_name'] = 'First name can only contain letters.'
        if not re.match(r'^[A-Za-z]+$', form_data['last_name']):
            errors['last_name'] = 'Last name can only contain letters.'

        # Validate username (letters, numbers, and underscores allowed)
        if not re.match(r'^[A-Za-z0-9_]+$', form_data['username']):
            errors['username'] = 'Username can only contain letters, numbers, and underscores.'

        # Check if passwords match
        if form_data['password'] != form_data['re_password']:
            errors['password_mismatch'] = 'Passwords do not match.'

        # Password length validation
        if len(form_data['password']) < 8:
            errors['password_length'] = 'Password must be at least 8 characters long.'

        # Check if the email is unique
        if User.objects.filter(email=form_data['email']).exists():
            errors['email_exists'] = 'This email is already registered.'

        # Check if the username is unique
        if User.objects.filter(username=form_data['username']).exists():
            errors['username_exists'] = 'This username is already taken.'

        # If there are any errors, return them with the form
        if errors:
            return render(request, 'user/index.html', {
                'errors': errors,
                'form_data': form_data
            })

        # Generate OTP and store user data in session
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['user_data'] = {
            'username': form_data['username'],
            'password': form_data['password'],
            'email': form_data['email'],
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name']
        }

        # Send OTP via email
        subject = 'Your OTP for Meat Souk'
        message = f'Hello {form_data["first_name"]},\nYour OTP for verifying your account is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form_data['email']]

        try:
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'user/otp_verification.html')
        except Exception as e:
            errors['email_error'] = 'Error sending email. Please try again later.'
            return render(request, 'user/index.html', {'errors': errors})

    return render(request, 'user/index.html')


def verify_otp(request):
    error_message = None
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_data = request.session.get('user_data')

        if user_data is None:
            error_message = 'Session expired or no user data found. Please try again.'
            return render(request, 'user/otp_verification.html', {'error_message': error_message})
        
        if not session_otp:
            error_message = 'OTP expired. Please request a new one.'
            return render(request, 'user/otp_verification.html', {'error_message': error_message})

        if str(user_otp) == str(session_otp):
            User = get_user_model()
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Now, login works with specified backend

            del request.session['otp']
            del request.session['user_data']
            return redirect('homepage')
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'user/otp_verification.html', {'error_message': error_message})

    return render(request, 'user/otp_verification.html')

def resend_otp(request):
    if request.method == 'POST':
        user_data = request.session.get('user_data')
        if not user_data:
            return JsonResponse({'success': False, 'error': 'Session expired. Please restart signup process.'})

        try:
            otp = generate_otp()
            request.session['otp'] = otp

            subject = 'Your New OTP for Meat Souk'
            message = f'Hello {user_data["first_name"]},\nYour new OTP for verifying your account is: {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_data['email']]

            send_mail(subject, message, email_from, recipient_list)
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Error resending OTP. Please try again later.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    
def invalidate_otp(request):
    if request.method == 'POST':
        if 'otp' in request.session:
            del request.session['otp']  # Remove OTP from session
        return JsonResponse({'message': 'OTP invalidated successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required(login_url='login')
@never_cache
def homepage(request):
    user = request.user
    cities = Pincode.objects.filter(is_listed=True).values_list('city', flat=True).distinct()
    # Check if pincode or city is already set in session
    pincode_set = request.session.get('pincode_set', False)
    return render(request, 'user/homepage.html', {'user': user, 'cities': cities, 'pincode_set': pincode_set})

@csrf_exempt
def set_pincode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pincode = data.get('pincode')
        request.session['pincode'] = pincode
        request.session['pincode_set'] = True
        return JsonResponse({'status': 'success'})
    
@csrf_exempt
def set_city(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get('city')
        request.session['city'] = city
        request.session['pincode_set'] = True
        return JsonResponse({'status': 'success'})

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if the user exists by email
            user = User.objects.get(email=email)

            # Check if the user is blocked
            if not user.is_active:
                error_message = 'Your account is blocked. Please contact support.'
                return render(request, 'user/login.html', {'error_message': error_message})

            # Authenticate the user
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('homepage')  # Redirect to home page after successful login
            else:
                error_message = 'Incorrect password. Please try again.'

        except User.DoesNotExist:
            error_message = 'No account found with this email. Please sign up.'

    return render(request, 'user/login.html', {'error_message': error_message})

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email exists in the database
        if User.objects.filter(email=email).exists():
            # Generate OTP and store it in the session
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            
            # Send OTP via email
            subject = 'Your OTP for Meat Souk Password Reset'
            message = f'Hello,\nYour OTP for resetting your password is: {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                # Redirect to the OTP verification page with a success message
                return redirect('forgot_pswd_verify')
            except Exception:
                error_message = 'Error sending OTP. Please try again later.'
                return render(request, 'user/forgotpassword.html', {'error_message': error_message})
        
        else:
            # If email doesn't exist, show an error message
            error_message = 'This email is not registered. Please sign up.'
            return render(request, 'user/forgotpassword.html', {'error_message': error_message})

    # Render the forgot password page for GET requests
    return render(request, 'user/forgotpassword.html')



def pincode(request):
    
    return render(request,'user/pincode.html')

@login_required(login_url='login')
@never_cache
def user_logout(request):
    # django's logout fuction automatically delete the session
    logout(request)
    # Redirect to login after logout
    return redirect('login')


User = get_user_model()

def verify_forgot_password_otp(request):
    error_message = None

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        # Verify the OTP
        if str(user_otp) == str(session_otp):
            # OTP is valid; delete it from session
            del request.session['otp']
            # Show the password reset modal by passing context
            return redirect('forgot_pswd_reset')
        else:
            # Invalid OTP, show error message
            error_message = 'Invalid OTP. Please try again.'

    return render(request, 'user/forgot_pswd_verify.html', {'error_message': error_message})


User = get_user_model()

def forgot_pswd_reset(request):
    # Retrieve the email from the session
    email = request.session.get('email')
    if not email:
        # Redirect to forgot password page if the email session is missing
        return redirect('forgotpassword')

    # Get the user associated with the email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # If no user is found, show an error message
        return render(request, 'user/forgot_pswd_reset.html', {'error_message': 'User not found.'})

    error_message = None
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        re_enter_password = request.POST.get('reenter_password')

        # Check if passwords match and meet the length requirement
        if new_password != re_enter_password:
            error_message = 'Passwords do not match.'
        elif len(new_password) < 8:
            error_message = 'Password must be at least 8 characters long.'
        
        if error_message:
            # Render with error message if validation fails
            return render(request, 'user/forgot_pswd_reset.html', {'error_message': error_message})

        # Set and save the new password for the user
        user.set_password(new_password)
        user.save()

         # Clear session data related to password reset if it exists
        if 'email' in request.session:
            del request.session['email']
        
        # Redirect to the login page with a success message
        return redirect('login')

    # Render the password reset form if GET request
    return render(request, 'user/forgot_pswd_reset.html')
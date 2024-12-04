from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.

@login_required(login_url='admin_login')
@never_cache
def admin_category(request):
    
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admin_category.html', context)

@login_required(login_url='admin_login')
@never_cache
def add_admin_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()
        is_listed = request.POST.get('is_listed') == 'on'

        if not category_name:
            messages.error(request, "Category name cannot be empty.")
            return redirect('add_admin_category')

        if len(category_name) < 2:
            messages.error(request, "Category name must be at least 2 characters long.")
            return redirect('add_admin_category')

        if not all(char.isalpha() or char.isspace() for char in category_name):
            messages.error(request, "Category name must contain only alphabets.")
            return redirect('add_admin_category')

        if Category.objects.filter(category_name__iexact=category_name).exists():
            messages.error(request, f"Category '{category_name}' already exists.")
            return redirect('add_admin_category')

        category_name = ' '.join(category_name.split())  # Normalize spaces

        try:

            new_category = Category(
                category_name=category_name,
                is_listed=is_listed
            )
            new_category.save()
            
            messages.success(request, f"Category '{category_name}' added successfully.")
            return redirect('admin_category')

        except Exception as e:

            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_admin_category')

    return render(request, 'admin_category_add.html')

@login_required(login_url='admin_login')
@never_cache
def edit_admin_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()
        is_listed = request.POST.get('is_listed') == 'on' 
        
        
        if not category_name:
            messages.error(request, "Category name cannot be empty.")
            return redirect('edit_admin_category', category_id=category_id)

        if len(category_name) < 2:
            messages.error(request, "Category name must be at least 2 characters long.")
            return redirect('edit_admin_category', category_id=category_id)

        if not all(char.isalpha() or char.isspace() for char in category_name):
            messages.error(request, "Category name must contain only alphabets.")
            return redirect('edit_admin_category', category_id=category_id)
        if Category.objects.filter(category_name__iexact=category_name).exclude(id=category_id).exists():
            messages.error(request, f"Category '{category_name}' already exists.")
            return redirect('edit_admin_category', category_id=category_id)

        category_name = ' '.join(category_name.split())

        try:
            category.category_name = category_name
            category.is_listed = is_listed
            category.save()
            
            messages.success(request, 'Category updated successfully.')
            return redirect('admin_category')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('edit_admin_category', category_id=category_id)
    
    return render(request, 'admin_category_edit.html', {'category': category})

def unlist_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if category.is_listed:
        category.is_listed = False
    category.save()
    return redirect('admin_category')

def list_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if not category.is_listed:
        category.is_listed = True
    category.save()
    return redirect('admin_category')
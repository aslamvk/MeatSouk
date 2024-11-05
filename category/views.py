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
    # Fetch all categories from the database
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admin_category.html', context)

@login_required(login_url='admin_login')
@never_cache
def add_admin_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        category_unit = request.POST.get('category_unit')
        is_listed = request.POST.get('is_listed') == 'on'  # Convert checkbox to boolean

        # Validate category name: Check if it already exists
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, "Category already exists.")
            return redirect('add_admin_category')

        # Validate that the category name contains only alphabetic characters
        if not category_name.isalpha():
            messages.error(request, "Category name must be alphabetic.")
            return redirect('add_admin_category')

        # Create new category
        new_category = Category(
            category_name=category_name,
            category_image=category_image,
            category_unit=category_unit,
            is_listed=is_listed
        )
        new_category.save()
        messages.success(request, "Category added successfully.")
        return redirect('admin_category')

    # If it's a GET request, render the add category form
    return render(request, 'admin_category_add.html')

@login_required(login_url='admin_login')
@never_cache
def edit_admin_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_unit = request.POST.get('category_unit')
        category_image = request.FILES.get('category_image')  # Handle file upload
        
        # Validate the inputs (you can customize the validation rules)
        if not category_name or not category_unit:
            messages.error(request, "Category name and unit are required.")
        else:
            # Update the category fields
            category.category_name = category_name
            category.category_unit = category_unit
            
            if category_image:
                # Optional: Delete the old image if a new one is uploaded
                if category.category_image:
                    default_storage.delete(category.category_image.path)
                
                # Save the new image
                category.category_image = category_image

            # Save the updated category object
            category.save()
            
            messages.success(request, 'Category updated successfully.')
            return redirect('admin_category')
    
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
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator

@login_required
def vendor_add_product(request):
    # Ensure that only vendors can add products
    if not request.user.is_vendor:
        return HttpResponseForbidden("You are not authorized to add products.")
    
    # Fetch top-level categories (parent categories) and their subcategories
    categories = Category.objects.filter(parent__isnull=True)
    subcategories = SubCategory.objects.all()
   

    if request.method == 'POST':
        # Get form data from POST request
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        discount_percentage = request.POST.get('discount_percentage')  # Discount percentage from form
        image = request.FILES.get('image')  # For file uploads
        vendor = request.user

        # Validate required fields
        if not name or not description or not price or not stock or not category_id:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'vendor_add_product.html', {'categories': categories})

        try:
            # Ensure price and stock are valid numbers
            price = float(price)
            stock = int(stock)

            # Ensure category is selected (either a parent or subcategory)
            category = Category.objects.get(id=category_id) if category_id else None

            # Handle discount percentage (if provided)
            if discount_percentage:
                discount_percentage = float(discount_percentage)
                discount_price = price * (1 - discount_percentage / 100)
            else:
                discount_percentage = None
                discount_price = None  # No discount if not provided

            # Create the product
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                vendor_creating_product=vendor,  # Current user is the vendor
                category=category,
                image=image,
                discount_percentage=discount_percentage,  # Saving the discount percentage
                # discount_price=discount_price  # Saving the calculated discount price
            )

            # Redirect to product list or success page after creation
            messages.success(request, "Product created successfully!")
            return redirect('vendor-product-list')  # Redirect to vendor's product list
        
        except ValueError:
            messages.error(request, "Invalid price or stock value. Please try again.")
            return render(request, 'vendor_add_product.html', {'categories': categories})

    # If the request is GET, pass categories and subcategories to the template
    return render(request, 'vendor_add_product.html', {'categories': categories, 'subcategories':subcategories})


def vendor_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        discount_percentage = request.POST.get('discount_percentage')  # Only handling discount percentage
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        image = request.FILES.get('image')

        # Get the category from the category ID
        category = Category.objects.get(id=category_id)
        sub_category = SubCategory.objects.get(id=subcategory_id)
        # Convert values to appropriate data types
        price = float(price)
        stock = int(stock)

        # Handle discount percentage logic
        if discount_percentage:
            discount_percentage = float(discount_percentage)
            # Calculate the discounted price based on the percentage
            discount_price = price * (1 - discount_percentage / 100)
        else:
            discount_percentage = None
            discount_price = None  # If no discount, set it to None

        # Update the product object with new values
        product.name = name
        product.price = price
        product.discount_percentage = discount_percentage
        product.discount_price = discount_price  # Store the discounted price
        product.description = description
        product.stock = stock
        product.category = category
        product.subcategory=sub_category

        # Handle image update (if a new image is uploaded)
        if image:
            product.image = image

        # Save the updated product
        product.save()

        # Display a success message and redirect to the product detail page
        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect('vendor-product-detail', product_id=product.id)

    # Pass the current product data and categories to the template
    categories = Category.objects.all()
    return render(request, 'vendor_edit_product.html', {'product': product, 'categories': categories})


@login_required
def vendor_delete_product(request, product_id):
   
    product = get_object_or_404(Product, id=product_id, vendor_creating_product= request.user)  # Ensure the product belongs to the logged-in vendor

    if request.method == "POST":
        # If confirmed, delete the product
        product.delete()
        messages.success(request, "Product has been deleted successfully!")
        return redirect('vendor-product-list')  # Redirect to the vendor's product list

    # If GET, render the confirmation page
    return render(request, 'vendor_delete_product.html', {'product': product})


@login_required
def vendor_product_list(request):
    # Ensure that only vendors can see this page
    if not request.user.is_vendor:
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Fetch products created by the logged-in vendor
    products = Product.objects.filter(vendor_creating_product=request.user)
    
    return render(request, 'vendor_product_list.html', {'products': products})

def vendor_product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'vendor_product_details.html', {'product': product})


def homeview(request):
    # Check if the user is authenticated and whether they are a vendor
    if request.user.is_authenticated:
        if request.user.is_vendor:
            # Vendor view: Show only products by the logged-in vendor
            products = Product.objects.filter(vendor_creating_product=request.user)
        else:
            # Buyer view: Show all products
            products = Product.objects.all()
    else:
        # Non-logged-in users: Show all products from all vendors
        products = Product.objects.all()

    # Fetch categories (this stays the same)
    categories = Category.objects.all()
    categories_n_sub=SubCategory.objects.select_related('category')
    categories_n_sub_list=[]
    categories_list=[]
    for cat in categories_n_sub:
        # categories_n_sub_list.append({
        #     'category':cat.category.name,
        #     'subcategory':[cat.name for category in cat]
        # })
        categories_n_sub_list.append({
            'category':cat.category.name,
            'subcategory':cat.name
        })
        categories_list.append(cat.category.name)
        
    unique_categories_list=list(set(categories_list))
    
    grouped_data = {}

# Loop through the subcategories and group them by their category
    for item in categories_n_sub_list:
        category = item['category']
        subcategory = item['subcategory']
        
        # If the category does not exist in the dictionary, add it with an empty list
        if category not in grouped_data:
            grouped_data[category] = []
        
        # Append the subcategory to the appropriate category
        grouped_data[category].append(subcategory)

    # Convert the grouped data to the desired format
    result = [{category: subcategories} for category, subcategories in grouped_data.items()]

    # Print the result
    print(result)
    
    
    
    subcategory = Category.objects.all()

    # Paginate the products (optional, if you /have many products)
    paginator = Paginator(products, 18)  # Show 12 products per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the page object based on the page number

    return render(request, 'home.html', {'page_obj': page_obj, 'categories': categories, 'cat_n_sub':result})

def products_by_category(request,category_name):
    
    # Check if the user is authenticated and whether they are a vendor
    if request.user.is_authenticated:
        category_to_sort_by=Category.objects.get(name=category_name)
        category_id=category_to_sort_by.id
        if request.user.is_vendor:
            # Vendor view: Show only products by the logged-in vendor
            products = Product.objects.filter(vendor_creating_product=request.user,category_id=category_id)
        else:
            # Buyer view: Show all products
            products = Product.objects.filter(category_id=category_id)
    else:
        # Non-logged-in users: Show all products from all vendors
        products = Product.objects.filter(category_id=category_id)

    # Fetch categories (this stays the same)
    categories = Category.objects.all()

    # Paginate the products (optional, if you have many products)
    paginator = Paginator(products, 18)  # Show 12 products per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the page object based on the page number

    return render(request, 'home.html', {'page_obj': page_obj, 'categories': categories})
def products_by_subcategory(request,subcategory_name):
    
    # Check if the user is authenticated and whether they are a vendor
    if request.user.is_authenticated:
        subcategory_to_sort_by=SubCategory.objects.get(name=subcategory_name)
        subcategory_id=subcategory_to_sort_by.id
        if request.user.is_vendor:
            # Vendor view: Show only products by the logged-in vendor
            products = Product.objects.filter(vendor_creating_product=request.user,subcategory_id=subcategory_id)
        else:
            # Buyer view: Show all products
            products = Product.objects.filter(subcategory_id=subcategory_id)
    else:
        # Non-logged-in users: Show all products from all vendors
        products = Product.objects.filter(subcategory_id=subcategory_id)

    # Fetch categories (this stays the same)
    categories = Category.objects.all()

    # Paginate the products (optional, if you have many products)
    paginator = Paginator(products, 18)  # Show 12 products per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the page object based on the page number

    return render(request, 'home.html', {'page_obj': page_obj, 'categories': categories})



# View to display a single product's details
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Fetch product by ID
    return render(request, 'product_details.html', {'product': product})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product

def add_to_cart(request, product_id):
    # Fetch the product
    product = get_object_or_404(Product, id=product_id)

    # Get the cart from the session (a dictionary)
    cart = request.session.get('cart', {})

    # If the product is already in the cart, increase its quantity
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        # If the product is not in the cart, add it
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.image.url
        }

    # Save the updated cart in the session
    request.session['cart'] = cart

    # Show success message
    messages.success(request, f"{product.name} has been added to your cart!")

    # Redirect to the homepage or cart page
    return redirect('home')  # Or wherever you want to redirect

def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart.html', {'cart': cart})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Cart

# View for displaying the product details
def product_detail(request, product_id):
    # Fetch the product by its ID, or return a 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)

    # Handle the add to cart functionality
    if request.method == 'POST' and request.user.is_authenticated:
        # Logic for adding product to the cart goes here
        # For example, adding the product to the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.add(product)  # Assuming Cart model has a many-to-many relation with Product
        cart.save()

        # Optionally, show a success message or redirect to cart
        return redirect('cart-view')  # Redirect to the cart view

    return render(request, 'product_detail.html', {'product': product})





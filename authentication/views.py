from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
User = get_user_model()



def registerviewbuyer(request):
    # print(request.method)
    context ={}
    if request.method == 'POST':
        # print('post request')
        username = request.POST.get('username')
        existing_user = User.objects.filter(username=username).exists()
        if existing_user:
            messages.error(request, 'Username already existss.')
            context = {'error' : 'Account with that username already exist'}
           
        # existing_email = User.objects.filter(email=email).exists()
        # if existing_email:
        #     context ={'error': 'Account with that email already exist'}
            
            
        if not existing_user:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')     
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            password = request.POST.get('password')
           
            context = {'success' : 'registration successful, proceed to log in'}
            
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email, 
                                            phone_number=phone_number,
                                            address=address,
                                            password=password
                                            )
            
            # if user_type == 'buyer':
            #     user.is_vendor = False
            #     messages.success(request, 'successful registration.')
            return redirect('go-login')
                
            # if user_type == 'vendor':
            #     user.is_vendor = True 
            #     messages.success(request, 'additional information required to complee registration.')
            #     return redirect('go-register-vendor')
            
    return render(request,  'register.html', context)

def registerviewvendor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        existing_user = User.objects.filter(username=username)
        
        if existing_user:
            messages.error(request, 'User already exist')
            return redirect('go-register-vendor')
        
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')     
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            password = request.POST.get('password')
            shop_name = request.POST.get('shop_name')
            shop_address = request.POST.get('shop_address')
            
            messages.success(request, 'vendor registration successful')
            
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email, 
                                            phone_number=phone_number,
                                            address=address,
                                            password=password,
                                            shop_name = shop_name,
                                            shop_address = shop_address,
                                            is_vendor = True
                                            )
            return redirect('go-login')  
    return render(request, 'vendor_register.html')

def loginview(request):
    context ={}
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        existing_user = User.objects.filter(username=username).exists()
        
        if not existing_user:
            context = {'error': 'Username or password not correct'}
            
        if existing_user:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user )
                context = {'success': 'login successful'}
                return redirect('go-home')
                
            else:
                context = {'error': 'incorrect password'}
                
            
            
        
    return render(request,  'login.html', context)

@login_required
def profile_view(request):
    
    personal_info ={}
    
    # user = User.objects.all().order_by('username')
    user = request.user
    
    personal_info = {
            'name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            'phone_number': user.phone_number,
            'shipping_address': user.address,
            'shop_address': user.shop_address,
            'shop_name': user.shop_name
            }
        
    #     'phone_number': user.profile.phone_number,  # Access the profile model
    #     'shipping_address': user.profile.shipping_address  # Access the profile model
    # print('check this: ', personal_info['name'])
    return render(request, 'profile.html', {'personal_info':personal_info})


@login_required
def edit_profile_view(request):
    user = request.user
    
    
    if request.method == 'POST':
        # Get data from the form fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        shipping_address = request.POST.get('shipping_address')
        shop_address = request.POST.get('shop_address')
        shop_name = request.POST.get('shop_name')

        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.shipping_address = shipping_address
        user.shop_address = shop_address
        user.shop_name = shop_name
        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect ('go-profile')
        
    return render(request, 'profile_edit.html')









# Create your views here.

from django.shortcuts import render, redirect
from .models import HotelUser, HotelVendor, Hotel, Amenities, HotelImages
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required
from .utils import generateSlug
from django.http import HttpResponseRedirect

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.warning(request, "Account already exists with given email or phone number")
            return redirect('/accounts/register/')
    
        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )

        hotel_user.set_password(password)
        hotel_user.save()


        sendEmailToken(email, hotel_user.email_token)

        messages.success(request, "An email sent to given email")
        return redirect('/accounts/register/')

    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email=email)

        if not hotel_user.exists():
            messages.warning(request, "No User found.")
            return redirect('/accounts/login/')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "User is not verified.")
            return redirect('/accounts/login/')
    
        hotel_user = authenticate(username=hotel_user[0].username, password=password)
        if hotel_user:
            messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/accounts/login/')


        messages.warning(request, "Invalid Credentials!")
        return redirect('/accounts/login/')

    return render(request, 'login.html')
   
def register_vendor_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelVendor.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.warning(request, "Account already exists with given email or phone number")
            return redirect('/accounts/register-vendor/')
    
        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            business_name = business_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )

        hotel_user.set_password(password)
        hotel_user.save()


        sendEmailToken(email, hotel_user.email_token, user_type='vendor')

        messages.success(request, "An email sent to given email")
        return redirect('/accounts/login-vendor/')

    return render(request, 'vendor/register_vendor.html')

def login_vendor_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(email=email)

        if not hotel_user.exists():
            messages.warning(request, "No User found.")
            return redirect('/accounts/login-vendor/')
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "User is not verified.")
            return redirect('/accounts/login-vendor/')
    
        hotel_user = authenticate(username=hotel_user[0].username, password=password)
        if hotel_user:
            # messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/accounts/dashboard/')


        messages.warning(request, "Invalid Credentials!")
        return redirect('/accounts/login-vendor/')

    return render(request, 'vendor/login_vendor.html')
 
def verify_email_token(request, token, user_type='user'):
    try:
        if user_type=='vendor':
            hotel_user = HotelVendor.objects.get(email_token = token)
        else:
            hotel_user = HotelUser.objects.get(email_token = token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        if user_type=='vendor':
            return redirect('/accounts/login-vendor/')
        else:
            return redirect('/accounts/login/')
    except Exception as e:
        return HttpResponse("Invalid Token")

def send_otp(request, email):
    
        hotel_user = HotelUser.objects.filter(email=email)

        if not hotel_user.exists():
            messages.warning(request, "No User found.")
            return redirect('/accounts/login/')

        new_otp = random.randint(1000, 9999)
        hotel_user.update(otp=new_otp)
        # hotel_user.save()

        sendOTPtoEmail(email, new_otp)
        return redirect(f'/accounts/verify-otp/{email}/')

def verify_otp(request, email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email=email)
        
        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/accounts/login/')
        messages.warning(request, "OTP does not match")
        return redirect(f'/accounts/verify-otp/{email}/')
    
    return render(request, 'verify_otp.html')

@login_required(login_url='login_vendor_page')
def dashboard(request):
    context ={'hotels': Hotel.objects.filter(hotel_owner=request.user)}
    return render(request, 'vendor/vendor_dashboard.html', context=context)

@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        amenities = request.POST.getlist('amenities')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)
        hotel_vendor = HotelVendor.objects.get(id = request.user.id)        
        # hotel_user = HotelVendor.objects.filter(email=email)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor,
        )

        for amenity in amenities:
            amenity = Amenities.objects.get(id=amenity)
            hotel_obj.amenities.add(amenity)
            hotel_obj.save()

        messages.success(request, "Hotel Added!")
        return redirect('/accounts/add-hotel/')
    
    amenities = Amenities.objects.all()

    return render(request, 'vendor/add_hotel.html', context={'amenities': amenities})

@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.method == 'POST':
        image = request.FILES['upload_image']
        print(image)
        HotelImages.objects.create(
            hotel = hotel_obj,
            image = image,
        )
        return HttpResponseRedirect(request.path_info)
    return render(request, 'vendor/upload_images.html', context={'images': hotel_obj.hotel_images.all()})

@login_required(login_url='login_vendor')
def delete_images(request, id):
    hotel_img = HotelImages.objects.get(id=id)
    hotel_img.delete()
    messages.success(request, "Image Deleted!")
    return redirect('/accounts/dashboard/')

@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not Authorised")
    
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        amenities = request.POST.getlist('amenities')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        # hotel_slug = generateSlug(hotel_name)
        hotel_vendor = HotelVendor.objects.get(id = request.user.id)        

        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.amenities.set(amenities)
        hotel_obj.save()

        messages.success(request, "Hotel Details Updated")
        return HttpResponseRedirect(request.path_info)

    amenities = Amenities.objects.all()
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'amenities': amenities})

@login_required()
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect("/accounts/login/")


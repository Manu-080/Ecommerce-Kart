from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# EMAIL CONFIGURATION
from django.core.mail import send_mail

# FORGOT PASSWORD
from .utils import generate_otp, send_otp_email
from django.core.cache import cache # For importing chache currently using django cache.


from .models import User
from .forms import UserSignupForm
from orders.models import UserAddress, OrderItem
from .update_user_form import UserUpdateForm

# Create your views here.


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user_auth = authenticate(request, email=email, password=password)

        if user_auth:
            login(request, user_auth)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            
    

    return render(request, 'user/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, username=username, phone_number=phone_number, password=password)
            user.save()

            # EMAIL MESSAGE FOR CREATING ACCOUNT
            subject = "Welcome to our Platform"
            message = f"Hello {username}.,\n\n Your account has been sucessfully created with {email}.\n\n If this is not you report at {settings.EMAIL_HOST_USER}."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('login')

    else:
        form = UserSignupForm()

    context = {
        'form' : form
    }
    return render(request, 'user/signup.html', context)


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    try:
        ordered_items = OrderItem.objects.filter(user=request.user)
    except OrderItem.DoesNotExist:
        pass

    context = {
        'ordered_items':ordered_items,
    }
    return render(request, 'user/dashboard.html', context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact = email)

            otp = generate_otp() 
            cache.set(email, otp, timeout=300) # Store otp for 5 minutes (email = key, otp = value, timeout is basically timeout) Stores data like key value pairs like dictionary.
            send_otp_email(email, otp)

            request.session['reset_email'] = email # store email in current session

            return redirect('verify_otp') # if email exists in database redirect to verifu_otp page. 
        else:
            return messages.error(request, 'User with this email doesnot exists.')
    return render(request, 'user/forgot_password.html')



def verify_otp(request):
    email = request.session.get('reset_email') # Retrirve the email from session

    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_stored = cache.get(email) # GETTING VALUE FROM CACHE.

        if otp_stored and otp_stored == otp_entered:
            cache.delete(email) # Remove otp from django cache after otp verification
            return redirect('reset_password')
        else:
            messages.error(request, 'Wrong Otp')

    return render(request, 'user/verify_otp.html')



def reset_password(request):
    email = request.session.get('reset_email') # Retrirve the email from session

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            raise messages.error(request, 'password donot match')
        
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        request.session.pop('reset_email', None) # clear session

        return redirect('login')

    return render(request, 'user/reset_password.html')



@login_required(login_url='login')
def add_address(request):
    

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')

        user_address = UserAddress.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email,
                                    phone_number=phone_number,address=address, landmark=landmark, city=city, pincode=pincode, state=state)
        
        user_address.save()
        messages.success(request, 'Address added.')

        return redirect('dashboard')
    
    return render(request, 'user/add_address.html')




@login_required(login_url='login')
def delete_address(request):
    user_address = UserAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        selected_address_obj = get_object_or_404(UserAddress, id=selected_address_id)

        selected_address_obj.delete()
        messages.success(request, 'Updated Account details')

        return redirect('delete_address')

    context = {
        'user_address':user_address,
    }
    return render(request, 'user/delete_address.html', context)




@login_required(login_url='login')
def update_user(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Account details')

            return redirect('dashboard')
        

    form = UserUpdateForm(instance=request.user)

    context = {
        'form':form,
    }
    return render(request, 'user/update_user.html', context)

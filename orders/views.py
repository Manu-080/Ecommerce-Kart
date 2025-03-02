from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import UserAddress
from cart.models import CartItem
# Create your views here.

# LAST STAGE BEFORE PAYMENT.
@login_required(login_url='login')
def place_order(request):
    total_price =0
    tax = 0
    total = 0

    # TO GET USER ADDRESS
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address') # GET THE VALUE OF THE RADIO BOX IN CHECKOUT PAGE (value = address.id)
        selected_address = UserAddress.objects.get(id=selected_address_id)
        print(selected_address, selected_address_id)

    cartitem = CartItem.objects.filter(cart__user = request.user)

    for item in cartitem:
        total_price += (item.product.discount_price * item.quantity)

    tax = round((0.9*total_price)/100)
    total = tax + total_price


    context = {
        'order_address':selected_address,
        'cart_items':cartitem,
        'total_price':total_price,
        'tax':tax,
        'total':total,
    }

    return render(request, 'order/payment.html', context)



# TO SAVE ADDRESS DETAIL OF USER.
@login_required(login_url='signin')
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

        return redirect('checkout')

    return render(request, 'order/add_address.html')
            
                                                    
        



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

        request.session['selected_address_id'] = selected_address_id # will store the selected address's id in session can retrieve if we need.
        print(request.session['selected_address_id'])

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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from .models import UserAddress, Order, OrderItem, Payment
from cart.models import CartItem
# Create your views here.

# LAST STAGE BEFORE PAYMENT.
@login_required(login_url='login')
def place_order(request):
    total = 0

    # TO GET USER ADDRESS
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address') # GET THE VALUE OF THE RADIO BOX IN CHECKOUT PAGE (value = address.id)
        selected_address = UserAddress.objects.get(id=selected_address_id, user=request.user)
        print(selected_address, selected_address_id)

        request.session['selected_address_id'] = selected_address_id # will store the selected address's id in session can retrieve if we need.
        print(request.session['selected_address_id'])

    cartitem = CartItem.objects.filter(cart__user = request.user)

     # If the cart is empty, prevent access and redirect to cart page
    if not cartitem.exists():
        messages.error(request, "Your cart is empty. Add items before proceeding to checkout.")
        return redirect("cart")  # Redirect to the cart page

    # Calculate total price
    total_price = sum(Decimal(item.product.discount_price) * Decimal(item.quantity) for item in cartitem)
    

    tax = round((Decimal('0.9') * Decimal(total_price))/Decimal('100'))
    total = tax + total_price
    print(total)

    context = {
        'order_address':selected_address,
        'cart_items':cartitem,
        'total_price':total_price,
        'tax':tax,
        'total':total,
    }

    return render(request, 'order/payment.html', context)




@login_required(login_url='login')
def place_order_COD(request):

    current_user = request.user

    selected_address_id = request.session.get('selected_address_id')
    user_address = UserAddress.objects.get(id=selected_address_id, user=current_user)

    cart_item = CartItem.objects.filter(cart__user = current_user) # gets all the items in cart corresponding to the user.

    # If the cart is empty, prevent access and redirect to cart page
    if not cart_item.exists():
        messages.error(request, "Your cart is empty. Add items before proceeding to checkout.")
        return redirect("cart")  # Redirect to the cart page

    # Calculate total price
    total_price = sum(Decimal(item.product.discount_price) * Decimal(item.quantity) for item in cart_item)
    
    
    tax = round((Decimal('0.9') * Decimal(total_price))/Decimal('100'))
    total_price = total_price + tax
    print(total_price)

    order = Order.objects.create(
            user=current_user,
            address=user_address,
            total_price=total_price 
            )

    for item in cart_item:
        
        order_item = OrderItem.objects.create(
            order=order, 
            product=item.product, 
            quantity=item.quantity, 
            price=item.product.discount_price
            )

    payment = Payment.objects.create(
        order=order, 
        payment_method="Cash on Delivery", 
        amount=total_price, 
        transaction_id=f"COD-{order.id}{current_user}"
        )
    messages.success(request, 'Order placed successfully')

    cart_item.delete()
    del request.session['selected_address_id'] # to delete session id


    return redirect('home')


def show_orders(request):
    pass

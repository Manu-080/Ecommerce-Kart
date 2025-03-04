import razorpay
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import UserAddress, Order, OrderItem, Payment
from cart.models import CartItem

# for sending email after placing order.
from .utils import send_order_placed_email

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

        



# COD PAYMENT FUNCTION.
@login_required(login_url='login')
def place_order_COD(request):

    current_user = request.user

    cart_item = CartItem.objects.filter(cart__user = current_user) # gets all the items in cart corresponding to the user.

    # If the cart is empty, prevent access and redirect to cart page
    if not cart_item.exists():
        messages.error(request, "Your cart is empty. Add items before proceeding to checkout.")
        return redirect("cart")  # Redirect to the cart page

    selected_address_id = request.session.get('selected_address_id')
    user_address = UserAddress.objects.get(id=selected_address_id, user=current_user)

    
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
            user=current_user,
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


    # SENDING EMAIL TO USER AFTER PLACING ORDER
    send_order_placed_email(current_user.email, cart_item)
    print(current_user.email)


    # delete cartitems and value in session
    cart_item.delete()
    del request.session['selected_address_id'] # to delete session id

    
    return redirect('home')



@csrf_exempt
@login_required(login_url='login')
def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        total = data.get('total_amount')

        try:
            total_amount_paise = int(Decimal(total) * 100)  # Convert to paise
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            payment_data = {
                "amount": total_amount_paise,
                "currency": "INR",
                "receipt": f"order_rcpt_{request.user.id}",
                "payment_capture": 1  # Auto capture
            }

            razoapay_order = client.order.create(data=payment_data)
            razoapay_order_id = razoapay_order['id']

            request.session['razoapay_order_id'] = razoapay_order_id

            return JsonResponse(razoapay_order)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        


@login_required(login_url='login')
def razor_pay_verification(request):

    current_user = request.user

    cart_item = CartItem.objects.filter(cart__user = current_user) # gets all the items in cart corresponding to the user.

    # If the cart is empty, prevent access and redirect to cart page
    if not cart_item.exists():
        messages.error(request, "Your cart is empty. Add items before proceeding to checkout.")
        return redirect("cart")  # Redirect to the cart page

    selected_address_id = request.session.get('selected_address_id')
    user_address = UserAddress.objects.get(id=selected_address_id, user=current_user)

    
    # Calculate total price
    total_price = sum(Decimal(item.product.discount_price) * Decimal(item.quantity) for item in cart_item)
    
    
    tax = round((Decimal('0.9') * Decimal(total_price))/Decimal('100'))
    total_price = total_price + tax
    print(total_price)

    order = Order.objects.create(
            user=current_user,
            address=user_address,
            total_price=total_price, 
            )
    order.is_paid =True
    order.save()

    for item in cart_item:
        
        order_item = OrderItem.objects.create(
            order=order, 
            user=current_user,
            product=item.product, 
            quantity=item.quantity, 
            price=item.product.discount_price
            )

    payment = Payment.objects.create(
        order=order, 
        payment_method="Razorpay", 
        amount=total_price, 
        transaction_id=request.session.get('razoapay_order_id')
        )
    messages.success(request, 'Order placed successfully')


    # SENDING EMAIL TO USER AFTER PLACING ORDER
    send_order_placed_email(current_user.email, cart_item)
    print(current_user.email)


    # delete cartitems and value in session
    cart_item.delete()
    del request.session['selected_address_id'] # to delete session id
    del request.session['razoapay_order_id'] # to delete session id


    return redirect('home')

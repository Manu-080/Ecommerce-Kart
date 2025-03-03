from django.conf import settings
from django.core.mail import send_mail


def send_order_placed_email(email, cart_item):

    if not cart_item:
        return # Don't send an email if no items in the cart
    
    cart_items = [item.product.name for item in cart_item]
    

    subject = "Order placed message"
    message = "You have placed order for " + ", ".join(cart_items)

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    except:
        print('failed to send mail')

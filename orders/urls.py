from django.urls import path

from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('place-order-cod/', views.place_order_COD, name='place_order_COD'),

    path("create-payment/", views.create_payment, name="create-payment"),


    path("razor_pay_verification/", views.razor_pay_verification, name="razor_pay_verificationt"),

    
]

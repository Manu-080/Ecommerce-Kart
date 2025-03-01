from django.urls import path

from . import views

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('add-address/', views.add_address, name='add_address'),
    
]

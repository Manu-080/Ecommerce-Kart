from django.urls import path

from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('add-address/', views.add_address, name='add_address'),
    
]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

]
from django.shortcuts import redirect
from django.views.generic import ListView

from . import views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from kitchen.models import Kitchen

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup_user/', views.signup, name='customer_signup'),
    path('signup_kitchen', views.KitchenSignupView.as_view(), name='kitchen_signup'),
    path('user_detail', views.user_detail, name='user_detail'),

    # path('', ListView.as_view(
    #     queryset=Kitchen.objects.all(),
    #     context_object_name='kitchen_list',
    #     template_name='kitchen/kitchen_list.html'),
    #      name='kitchen_list',
    #      ),

    # path('', lambda request: redirect('kitchen/', permanent=True)),

    path('register/', views.register, name='register')
]
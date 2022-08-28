from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='index'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout, name='checkout'),
]

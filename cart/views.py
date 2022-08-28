from importlib.metadata import requires
from django.shortcuts import render, redirect
from django.http import (
    HttpResponse, 
    HttpResponseRedirect,
    Http404, 
    JsonResponse )
from .models import Cart
from accounts.forms import LoginForm, GuestForm
from products.models import Product
from billing.models import BillingProfile
from orders.models import Order
from accounts.models import *



def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj
    

def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    template_name = 'cart/cart.html'
    context = {
        'cart': cart_obj,
    }
    return render(request, template_name, context)


def cart_update(request):

    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:index')

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)            
        else:
            cart_obj.products.add(product_obj)

        request.session['cart_items'] = cart_obj.products.count() 

        print("-----nombre d'article dans le panier----------")
        print(request.session['cart_items'])
    return redirect('cart:index')


def checkout(request):
    order_obj = None
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:index')
       
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    
    if user.is_authenticated:
        # utilisateur connecté et se rappeler de sa méthode de paiement
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        # connecté en tant qu'invité et gestion de méthode  de paiement
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        
    template_name = 'cart/checkout.html'
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    
    return render(request, template_name, context)
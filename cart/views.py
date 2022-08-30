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
from address.models import Address
from address.forms import AddressForm



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

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    # GESTIONNAIRE DU PROFIL D'UTILISATEUR DU SITE
    billing_profile, billing_guest_profile_created = BillingProfile.objects.new_or_get(request)
    
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address =Address.objects.get(id=billing_address_id) 
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
            
    if request.method == "POST":
        #del request.session['cart_id']
        return redirect("/cart/success")
        
    template_name = 'cart/checkout.html'
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
    }
    
    return render(request, template_name, context)
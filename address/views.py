from django.shortcuts import render
from .forms import *
from django.contrib.auth.views import LoginView, LogoutView, login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from time import timezone
from django.http import HttpResponse
from billing.models import BillingProfile
from django.shortcuts import render, redirect

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            billing_address_id = request.session.get('billing_address_id', None)
            shipping_address_id = request.session.get('shipping_address_id', None)
        else:
            return redirect("cart:checkout")
        # On redirige l'utilisateur vers la page checkout
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")
    return redirect("cart:checkout")



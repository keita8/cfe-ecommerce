from locale import normalize
from time import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.views import LoginView, LogoutView, login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import GuestEmail
from django.utils import timezone

def guest_register_view(request):
    form = GuestForm(request.POST or None)

    context = {
        'form': form,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email           = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        # On redirige l'utilisateur vers la page checkout
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("accounts:register")
    
    return redirect('accounts:register')


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            print("connecté avec succès")
            print(request.user.is_authenticated)
            context['form'] = LoginForm()
            # On redirige l'utilisateur vers la page checkout
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Erreur lors de la connexion")
            
    
    template_name = 'accounts/login.html'

    
    return render(request, template_name, context)









def register_page(request):
    
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(username, email, password)
        print(user)
    
    template_name = 'accounts/register.html'

    return render(request, template_name, context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
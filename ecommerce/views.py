from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def homepage(request):
    template_name = 'layouts/index.html'
    context = {}
    return render(request, template_name, context)


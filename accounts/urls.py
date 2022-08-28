from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/guest/', views.guest_register_view, name='guest'),
    path('login/', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_page, name="register"),
]

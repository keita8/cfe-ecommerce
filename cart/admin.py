from django.contrib import admin
from .models import Cart
from products.models import Product

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'update', 'timestamp']
    readonly_fields = ['subtotal', 'total']
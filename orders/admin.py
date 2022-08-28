from ast import Or
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'cart', 'status', 'total', 'timestamp']
    list_display_links = ['order_id', 'cart']
    readonly_fields = ['order_id', 'total']
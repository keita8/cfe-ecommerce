from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active', 'timestamp']
    list_display_links = ['title', 'price']
    list_editable = ['active']
from django.contrib import admin
from .models import Address

admin.site.register(Address)

# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = []
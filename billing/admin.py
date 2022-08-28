from django.contrib import admin
from .models import BillingProfile

@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'active', 'update', 'timestamp']
    list_display_links = ['user', 'email']
    readonly_fields = ['email']

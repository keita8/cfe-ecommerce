from django.contrib import admin
from .models import Categorie

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created']
    list_display_links = ('category_name', )
    prepopulated_fields = {'slug': ('category_name', )}
    search_fields = ('category_name', )
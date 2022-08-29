from django.contrib import admin
from .models import Image

from django.contrib import admin

# from .forms import ImageForm
from .models import Image

# class ImageAdmin(admin.ModelAdmin):
#     form = ImageForm

admin.site.register(Image)
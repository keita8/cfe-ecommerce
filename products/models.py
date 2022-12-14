from unicodedata import category
from django.db.models import Q
from decimal import Decimal
from math import fsum
from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
import random
from tinymce.models import HTMLField
import string
import os
from category.models import Categorie
from .utils import unique_slug_generator
from upload.models import Image


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext
    
     

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910207878)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"products/{new_filename}/{final_filename}"
    

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def search(self, query):
        lookups = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(tag__title__icontains=query)) # ici on recupère les tags associés aux articles 
        return self.filter(lookups).distinct()
    
    def featured(self):
        return self.filter(feature=True)
    
    
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()
    
    def features(self):
        return self.get_queryset().featured()
    
    def search(self, query):
        return self.get_queryset().active().search(query)
    
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Product(models.Model):
    title       = models.CharField(max_length=255, verbose_name='Article')
    slug        = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='Slug')
    description = HTMLField(verbose_name="Description")
    price       = models.DecimalField(
                default=99.99, 
                max_digits=100, 
                decimal_places=2,
                validators=[MaxValueValidator(1000000000000000000), MinValueValidator(1)],
                verbose_name='Prix unitaire'
                )
    # photo       = models.FileField(
    #             upload_to=upload_image_path,
    #             validators=[FileExtensionValidator( ['jpg', 'png'] )],
    #             blank=True,
    #             null=True, 
    #             verbose_name='Image'
    #             )
    image       = models.ManyToManyField(
                Image,
                verbose_name='Image'
                )
    
    feature     = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    stock       = models.IntegerField(
                default=1, 
                verbose_name='En stock',
                validators=[MaxValueValidator(1000000000000000000), MinValueValidator(1)]
                )
    category    = models.ManyToManyField(Categorie, verbose_name='Catégories')
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    objects = ProductManager()
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk, 'slug':self.slug})   
    
    def __str__(self):
        return f" {self.title} " 
    
    
    

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product) 
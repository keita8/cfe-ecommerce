from django.db import models
from django.utils.text import slugify


class Categorie(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name='Catégorie')
    slug          = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    active        = models.BooleanField(default=True)
    created       = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super(Categorie, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category_name}"
    
    
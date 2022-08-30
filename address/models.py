from tabnanny import verbose
from django.db import models
from billing.models import BillingProfile
from django_countries.fields import CountryField

ADDRESS_TYPE = (
    ('billing', 'Facturation'),
    ('shipping', 'Livraison')
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, verbose_name="Client")
    address_type    = models.CharField(max_length=120, verbose_name="Type d'adresse", choices=ADDRESS_TYPE)
    address_line_1  = models.CharField(max_length=120, verbose_name="Adresse 1")
    address_line_2  = models.CharField(max_length=120, verbose_name="Adresse 2", blank=True, null=True)
    country = CountryField()
    city            = models.CharField(max_length=120, verbose_name="Ville")
    state           = models.CharField(max_length=120, verbose_name="Etat")
    postal_code     = models.CharField(max_length=120, verbose_name="Code postale")
    
    class Meta:
        verbose_name = 'Adresse de livraison'
        verbose_name = 'Adresses de livraison'
        
    
    def __str__(self):
        return f"{self.billing_profile}"
    
    
    
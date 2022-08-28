from statistics import mode
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='client')
    email = models.EmailField(max_length=255, verbose_name='Adresse email')
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    # customer_id
    
    class Meta:
        verbose_name = 'Adresse de facturation'
        verbose_name_plural = 'Adresse de facturation'
    
    
    def __str__(self):
        return f" {self.email} "
    
    
# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.cutomer_id = newID
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
        
        

post_save.connect(user_created_receiver, sender=User)
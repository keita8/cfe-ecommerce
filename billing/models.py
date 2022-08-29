from statistics import mode
from time import sleep
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        
        if user.is_authenticated:
            # utilisateur connecté et se rappeler de sa méthode de paiement
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            # connecté en tant qu'invité et gestion de méthode  de paiement
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='client')
    email = models.EmailField(max_length=255, verbose_name='Adresse email')
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    # customer_id
    
    objects = BillingProfileManager()
    
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
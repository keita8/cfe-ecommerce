from tkinter.tix import Tree
from turtle import update
from django.db import models
from cart.models import Cart
from products.utils import unique_order_id_generator
import math
from django.db.models.signals import pre_save, post_save
from billing.models import BillingProfile


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
               
        return obj, created



ORDER_STATUS_CHOICES = (
    ('created', 'Créée'),
    ('paid', 'Payée'),
    ('shipped', 'Livrée'),
    ('refunded', 'Remboursée')
)


class Order(models.Model):
    order_id       = models.CharField(max_length=150, verbose_name="N° de la commande", blank=True)
    billing_profile=models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True)
    cart           = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Panier")
    status         = models.CharField(max_length=100, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=9.99, max_digits=100, decimal_places=2, verbose_name='Frais de livraison')
    total          = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name="Total")
    timestamp      = models.DateTimeField(auto_now_add=True, verbose_name="Date de la commande")
    active         = models.BooleanField(default=True)
    
    objects = OrderManager()

    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total
        
        
    def __str__(self):
        return f" {self.order_id} "
    
    
def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=True)


pre_save.connect(pre_save_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id    = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
            
            print(order_obj.update_total())


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
        

post_save.connect(post_save_order, sender=Order)
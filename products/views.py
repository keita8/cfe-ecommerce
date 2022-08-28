from urllib import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from django.http import Http404
from cart.models import Cart

# LISTER TOUS LES ARTICLES
class ProductListView(ListView):
    template_name = 'layouts/shop.html'
    
    def get_queryset(self, *args, **kwargs):
        return Product.objects.all()
    
    
# DETAILS D'UN ARTICLE
class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'layouts/detail.html'
    
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context 
    
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Cet article n'existe pas")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Une erreur s'est produite...")

        return instance
        

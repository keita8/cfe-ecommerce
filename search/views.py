from urllib import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import *
from django.db.models import Q
# Create your views here.

# CHERCHER UN ARTICLE OU UN GROUPE D'ARTICLE SELON UN MOTIF
class SearchProductListView(ListView):
    template_name = 'search/view.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.features()
    

from itertools import product
from math import prod
from time import sleep

from django.db import connection
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from .models import *


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('id')
    template_name = 'index.html'
    paginate_by = 50


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 5

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, name=self.kwargs['category'])
        products = cache.get(f'products_{category}')
        if not products:
            dict_to_cache = {}
            for product in Product.objects.filter(category=category).iterator():
                dict_to_cache[f'{product}'] = {
                    'price': float(product.price),
                    'status': product.status,
                    'remains': product.remains
                }
            cache.set(f'products_{category}', dict_to_cache, 60*15)
            products = dict_to_cache
            sleep(2)
            print('CACHING')
        else:
            products = cache.get(f'products_{category}')
            print('CACHED')
        
        context['dict_to_cache'] = products
        return context

        
    def get_queryset(self):
        #category = get_object_or_404(Category, name=self.kwargs['category'])
        #vals = Product.objects.filter(category=category).values()
        return []



from time import sleep

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.core.cache import cache

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

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs['category'])
        products = cache.get(f'products_{category}')
        if not products:
            products = Product.objects.filter(category=category)
            cache.set(f'products_{category}', list(products), 60*15)
            sleep(2)
        return products
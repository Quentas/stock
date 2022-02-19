from time import sleep

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.core.cache import cache

from .models import *
from .tasks import send


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('id')
    template_name = 'index.html'
    paginate_by = 50


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, name=self.kwargs['category'])
        products = cache.get(f'products_{category}')
        if not products:
            # Writes every product of this category into dictionary
            # and sets it into cache
            dict_to_cache = {}
            for product in Product.objects.filter(category=category).iterator():
                dict_to_cache[f'{product}'] = {
                    'price': float(product.price),
                    'status': product.status,
                    'remains': product.remains
                }
            cache.set(f'products_{category}', dict_to_cache, 60*15)
            products = dict_to_cache
            sleep(2)  ## Performs time consuming task
            print('CACHING')
        else:
            print('CACHED')
        # Cuts a dictionary of objects according to pagination
        page = 1
        if self.request.GET.get('page'):
            page = int(self.request.GET.get('page'))
        start = (page - 1) * self.paginate_by
        stop = page * self.paginate_by
        context['dict_to_cache'] = dict(list(products.items())[start:stop])
        send.delay(self.kwargs['category'])
        return context

    def get_queryset(self):
        # This is done only for page pagination to work properly
        count = Product.objects.filter(category__name=self.kwargs['category']).count()
        return [None] * count



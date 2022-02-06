from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView
from .models import *
from time import sleep


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    paginate_by = 50


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 50

    
    def get_queryset(self):
        sleep(2)
        category = get_object_or_404(Category, name=self.kwargs['category'])
        return Product.objects.filter(category=category)

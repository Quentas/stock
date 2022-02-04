from http.client import ImproperConnectionState
from unicodedata import category
from django.core.management.base import BaseCommand
from products.models import *
from products.service import random_string
from django.db import transaction
from random import choice


class Command(BaseCommand):
    help = u'Создание категорий и продуктов'

    def add_arguments(self, parser):
        parser.add_argument(
            'categories', type=int,
            help=u'Количество создаваемых категорий'
            )
        parser.add_argument(
            'products', type=int, 
            help=u'Количество создаваемых продуктов в категории')

    def handle(self, *args, **kwargs):
        category_names = Category.objects.values_list('name', flat=True)
        product_names = Product.objects.values_list('name', flat=True)
        new_category_names = [random_string(category_names) for _ in range(kwargs['categories'])]
        new_product_names = [random_string(product_names) for _ in range(kwargs['products'])]
        
        transaction.set_autocommit(False)
        try:
            Category.objects.bulk_create(
                [Category(name=name) for name in new_category_names]
                )
            Product.objects.bulk_create(
                [Product(
                    name=name, 
                    category=choice(Category.objects.all()),
                    price=0,
                    remains=0,
                    status='out_of_stock')
                for name in new_product_names]
                )
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        finally:
            transaction.set_autocommit(True)
        
        
        
        
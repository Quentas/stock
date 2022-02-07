from random import choice

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from products.models import *
from products.service import random_string


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

    @transaction.atomic
    def handle(self, *args, **kwargs):
        category_names = Category.objects.values_list('name', flat=True)
        product_names = Product.objects.values_list('name', flat=True)
        new_category_names = [random_string(category_names) for _ in range(kwargs['categories'])]
        new_product_names = [random_string(product_names) for _ in range(kwargs['products'])]
        Category.objects.bulk_create(
            [Category(name=name) for name in new_category_names]
        )
        categories = Category.objects.all()
        Product.objects.bulk_create(
            [Product(
                name=name, 
                category=choice(categories),
                price=0,
                remains=0,
                status='out_of_stock')
            for name in new_product_names
            ]
        )
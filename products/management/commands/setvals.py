from django.core.cache import cache
from random import (
    choice, 
    uniform, 
    randrange
)

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from products.models import Product
from products.service import round_up


class Command(BaseCommand):
    help = u'Обновление цен, статуса и остатков'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ls = []
        for item in Product.objects.iterator():
            data = {
                'id': item.id,
                'price': round_up(uniform(0.01, 999.99), 2),
                'status': choice(['in_stock', 'out_of_stock']),
                'remains': randrange(50)
            }
            item.price = data['price']
            item.status = data['status']
            item.remains = data['remains']
            ls.append(item)

            cached_queryset = cache.get(f'products_{item.category}')
            if cached_queryset:
                print(item)
                print(cached_queryset)
                if item in cached_queryset:
                    print(item, True)

            #print(f"Item '{item}': Price {data['price']} // Status: {data['status']} // Remains: {data['remains']}")
        Product.objects.bulk_update(ls, ['price', 'status', 'remains'])
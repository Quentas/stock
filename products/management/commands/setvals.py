from random import (
    choice, 
    uniform, 
    randrange
)

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from products.models import Product
from products.service import round_up
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


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

            if cache.get(f'products_{item.category}'):
                cached_dict = cache.get(f'products_{item.category}')
                if cached_dict[f'{item}']:
                    # Updates it's values
                    cached_dict[f'{item}']['price'] = data['price']
                    cached_dict[f'{item}']['status'] = data['status']
                    cached_dict[f'{item}']['remains'] = data['remains']
                else:
                    # Creates new object to dictionary
                    cached_dict[f'{item}'] = {
                        'price': data['price'], 
                        'status': data['status'], 
                        'remains': data['remains']
                        }
                cache.set(f'products_{item.category}', cached_dict, 60*15)
            print(f"Item '{item}': Price {data['price']} // Status: {data['status']} // Remains: {data['remains']}")
        Product.objects.bulk_update(ls, ['price', 'status', 'remains'])
        print(len(connection.queries))
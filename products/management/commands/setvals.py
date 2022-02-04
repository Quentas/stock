from random import (
    choice, 
    uniform, 
    randrange
)
from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Product
from products.service import round_up


class Command(BaseCommand):
    help = u'Обновление цен, статуса и остатков'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for item in Product.objects.iterator():
            data = {
                'price': round_up(uniform(0.01, 999.99), 2),
                'status': choice(['in_stock', 'out_of_stock']),
                'remains': randrange(50)
            }
            print(f"Item '{item}': Price {data['price']} // Status: {data['status']} // Remains: {data['remains']}")
            Product.objects.filter(id=item.id).update(**data)
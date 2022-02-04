from django.db import models

class Category(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=20)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    status = models.CharField(choices=[
        ('in_stock', 'In stock'),
        ('out_of_stock', 'Out of stock')
    ], max_length=12)
    remains = models.IntegerField()

    def __str__(self):
        return f'{self.name}  -  {self.category}'
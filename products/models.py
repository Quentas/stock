from django.db import models

class Category(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def amount_of_products(self):
        return Product.objects.filter(category=self).count()

class Product(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=20)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    status = models.CharField(choices=[
        ('in_stock', 'In stock'),
        ('out_of_stock', 'Out of stock')
    ], max_length=12)
    remains = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'

    def __eq__(self, other):
        vals = [
            self.id == other.id,
            self.name == other.name,
            self.category == other.category,
            self.price == other.price,
            self.status == other.status,
            self.remains == other.remains,
        ]
        return all(vals)
# Generated by Django 4.0.2 on 2022-02-04 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('in_stock', 'In stock'), ('out_of_stock', 'Out of stock')], max_length=12)),
                ('remains', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
            ],
        ),
    ]

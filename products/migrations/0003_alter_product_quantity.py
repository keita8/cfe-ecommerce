# Generated by Django 4.1 on 2022-08-25 13:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(1000000000000000000), django.core.validators.MinValueValidator(1)], verbose_name='En stock'),
        ),
    ]

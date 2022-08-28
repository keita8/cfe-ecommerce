# Generated by Django 4.1 on 2022-08-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100, verbose_name='Frais de livraison'),
        ),
    ]
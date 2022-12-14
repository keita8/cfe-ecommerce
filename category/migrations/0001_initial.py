# Generated by Django 4.1 on 2022-08-29 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True, verbose_name='Catégorie')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
    ]

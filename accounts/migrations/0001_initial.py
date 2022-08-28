# Generated by Django 4.1 on 2022-08-28 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuestEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('active', models.DateTimeField(default=True)),
            ],
            options={
                'verbose_name': 'Invité',
                'verbose_name_plural': 'Invités',
            },
        ),
    ]

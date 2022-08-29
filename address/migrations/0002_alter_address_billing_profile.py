# Generated by Django 4.1 on 2022-08-29 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_alter_billingprofile_email_and_more'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='billing_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile', verbose_name='Client'),
        ),
    ]
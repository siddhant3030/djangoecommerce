# Generated by Django 2.2.5 on 2019-09-28 10:14

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0010_order_billing_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='countries',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='country',
            field=django_countries.fields.CountryField(default='India', max_length=2),
            preserve_default=False,
        ),
    ]

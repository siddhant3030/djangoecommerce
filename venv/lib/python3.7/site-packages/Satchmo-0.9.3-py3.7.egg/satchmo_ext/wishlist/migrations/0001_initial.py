# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductWish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_details', models.TextField(null=True, verbose_name='Details', blank=True)),
                ('create_date', models.DateTimeField(verbose_name='Creation Date')),
                ('contact', models.ForeignKey(related_name='wishlist', verbose_name='Contact', to='contact.Contact', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(related_name='wishes', verbose_name='Product', to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Product Wish',
                'verbose_name_plural': 'Product Wishes',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('po_number', models.CharField(max_length=20, verbose_name='Customer PO Number')),
                ('balance', models.DecimalField(null=True, verbose_name='Outstanding Balance', max_digits=18, decimal_places=10, blank=True)),
                ('paydate', models.DateField(null=True, verbose_name='Paid on', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='Notes', blank=True)),
                ('order', models.ForeignKey(to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

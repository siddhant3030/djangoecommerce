# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_num', models.CharField(max_length=50, verbose_name='Supplier ID')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('unit_cost', models.DecimalField(verbose_name='Unit Cost', max_digits=6, decimal_places=2)),
                ('inventory', models.DecimalField(verbose_name='Inventory', max_digits=18, decimal_places=6)),
                ('supplier', models.ForeignKey(verbose_name='Supplier', to='contact.Organization', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Raw Item',
                'verbose_name_plural': 'Raw Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField(verbose_name='Date Created')),
                ('order_sub_total', models.DecimalField(verbose_name='Subtotal', max_digits=6, decimal_places=2)),
                ('order_shipping', models.DecimalField(verbose_name='Shipping', max_digits=6, decimal_places=2)),
                ('order_tax', models.DecimalField(verbose_name='Tax', max_digits=6, decimal_places=2)),
                ('order_notes', models.CharField(max_length=200, verbose_name='Notes', blank=True)),
                ('order_total', models.DecimalField(verbose_name='Total', max_digits=6, decimal_places=2)),
                ('supplier', models.ForeignKey(verbose_name='Supplier', to='contact.Organization', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Supplier Order',
                'verbose_name_plural': 'Supplier Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierOrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line_item_quantity', models.IntegerField(verbose_name='Line Item Quantity')),
                ('line_item_total', models.DecimalField(verbose_name='Line Item Total', max_digits=6, decimal_places=2)),
                ('line_item', models.ForeignKey(verbose_name='Line Item', to='supplier.RawItem', on_delete=models.CASCADE)),
                ('order', models.ForeignKey(to='supplier.SupplierOrder', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierOrderStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(blank=True, max_length=20, verbose_name='Status', choices=[('Sent in', 'Sent in'), ('Shipped', 'Shipped'), ('Received', 'Received')])),
                ('notes', models.CharField(max_length=100, verbose_name='Notes', blank=True)),
                ('date', models.DateTimeField(verbose_name='Date', blank=True)),
                ('order', models.ForeignKey(to='supplier.SupplierOrder', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Supplier Order Status',
                'verbose_name_plural': 'Supplier Order Statuses',
            },
            bases=(models.Model,),
        ),
    ]

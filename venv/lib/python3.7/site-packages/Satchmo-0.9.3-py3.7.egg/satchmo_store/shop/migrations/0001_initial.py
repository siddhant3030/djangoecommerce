# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import satchmo_utils.fields
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('contact', '0001_initial'),
        ('sites', '0001_initial'),
        ('l10n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=10, null=True, verbose_name='Description', blank=True)),
                ('date_time_created', models.DateTimeField(verbose_name='Creation Date')),
                ('customer', models.ForeignKey(verbose_name='Customer', blank=True, to='contact.Contact', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Shopping Cart',
                'verbose_name_plural': 'Shopping Carts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(verbose_name='Quantity', max_digits=18, decimal_places=6)),
                ('cart', models.ForeignKey(verbose_name='Cart', to='shop.Cart', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(verbose_name='Product', to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItemDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(verbose_name='detail')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('price_change', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Item Detail Price Change', max_digits=6, decimal_places=2, blank=True)),
                ('sort_order', models.IntegerField(help_text='The display order for this group.', verbose_name='Sort Order')),
                ('cartitem', models.ForeignKey(related_name='details', to='shop.CartItem', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Cart Item Detail',
                'verbose_name_plural': 'Cart Item Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('site', models.OneToOneField(primary_key=True, serialize=False, to='sites.Site', verbose_name='Site', on_delete=models.CASCADE)),
                ('store_name', models.CharField(unique=True, max_length=100, verbose_name='Store Name')),
                ('store_description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('store_email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('street1', models.CharField(max_length=50, null=True, verbose_name='Street', blank=True)),
                ('street2', models.CharField(max_length=50, null=True, verbose_name='Street', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=30, null=True, verbose_name='State', blank=True)),
                ('postal_code', models.CharField(max_length=9, null=True, verbose_name='Zip Code', blank=True)),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='Phone Number', blank=True)),
                ('in_country_only', models.BooleanField(default=True, verbose_name='Only sell to in-country customers?')),
                ('country', models.ForeignKey(verbose_name='Country', to='l10n.Country', on_delete=models.CASCADE)),
                ('sales_country', models.ForeignKey(related_name='sales_country', verbose_name='Default country for customers', blank=True, to='l10n.Country', null=True, on_delete=models.SET_NULL)),
                ('shipping_countries', models.ManyToManyField(related_name='shop_configs', verbose_name='Shipping Countries', to='l10n.Country', blank=True)),
            ],
            options={
                'verbose_name': 'Store Configuration',
                'verbose_name_plural': 'Store Configurations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ship_addressee', models.CharField(max_length=61, verbose_name='Addressee', blank=True)),
                ('ship_street1', models.CharField(max_length=80, verbose_name='Street', blank=True)),
                ('ship_street2', models.CharField(max_length=80, verbose_name='Street', blank=True)),
                ('ship_city', models.CharField(max_length=50, verbose_name='City', blank=True)),
                ('ship_state', models.CharField(max_length=50, verbose_name='State', blank=True)),
                ('ship_postal_code', models.CharField(max_length=30, verbose_name='Zip Code', blank=True)),
                ('ship_country', models.CharField(max_length=2, verbose_name='Country', blank=True)),
                ('bill_addressee', models.CharField(max_length=61, verbose_name='Addressee', blank=True)),
                ('bill_street1', models.CharField(max_length=80, verbose_name='Street', blank=True)),
                ('bill_street2', models.CharField(max_length=80, verbose_name='Street', blank=True)),
                ('bill_city', models.CharField(max_length=50, verbose_name='City', blank=True)),
                ('bill_state', models.CharField(max_length=50, verbose_name='State', blank=True)),
                ('bill_postal_code', models.CharField(max_length=30, verbose_name='Zip Code', blank=True)),
                ('bill_country', models.CharField(max_length=2, verbose_name='Country', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='Notes', blank=True)),
                ('sub_total', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Subtotal', max_digits=18, decimal_places=10, blank=True)),
                ('total', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Total', max_digits=18, decimal_places=10, blank=True)),
                ('discount_code', models.CharField(help_text='Coupon Code', max_length=20, null=True, verbose_name='Discount Code', blank=True)),
                ('discount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Discount amount', max_digits=18, decimal_places=10, blank=True)),
                ('method', models.CharField(blank=True, max_length=50, verbose_name='Order method', choices=[(b'Online', 'Online'), (b'In Person', 'In Person'), (b'Show', 'Show')])),
                ('shipping_description', models.CharField(max_length=200, null=True, verbose_name='Shipping Description', blank=True)),
                ('shipping_method', models.CharField(max_length=200, null=True, verbose_name='Shipping Method', blank=True)),
                ('shipping_model', models.CharField(blank=True, max_length=30, null=True, verbose_name='Shipping Models')),
                ('shipping_cost', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Shipping Cost', max_digits=18, decimal_places=10, blank=True)),
                ('shipping_discount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Shipping Discount', max_digits=18, decimal_places=10, blank=True)),
                ('tax', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Tax', max_digits=18, decimal_places=10, blank=True)),
                ('time_stamp', models.DateTimeField(null=True, verbose_name='Timestamp', blank=True)),
                ('status', models.CharField(blank=True, help_text='This is set automatically.', max_length=20, verbose_name='Status', choices=[(b'Temp', 'Temp'), (b'New', 'New'), (b'Blocked', 'Blocked'), (b'In Process', 'In Process'), (b'Billed', 'Billed'), (b'Shipped', 'Shipped'), (b'Complete', 'Complete'), (b'Cancelled', 'Cancelled')])),
                ('contact', models.ForeignKey(verbose_name='Contact', to='contact.Contact', on_delete=models.CASCADE)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Product Order',
                'verbose_name_plural': 'Product Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(blank=True, max_length=25, verbose_name='Payment Method')),
                ('amount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='amount', max_digits=18, decimal_places=10, blank=True)),
                ('time_stamp', models.DateTimeField(null=True, verbose_name='timestamp', blank=True)),
                ('transaction_id', models.CharField(max_length=45, null=True, verbose_name='Transaction ID', blank=True)),
                ('details', models.CharField(max_length=255, null=True, verbose_name='Details', blank=True)),
                ('reason_code', models.CharField(max_length=255, null=True, verbose_name='Reason Code', blank=True)),
                ('complete', models.BooleanField(default=False, verbose_name='Complete')),
            ],
            options={
                'verbose_name': 'Order Payment Authorization',
                'verbose_name_plural': 'Order Payment Authorizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(verbose_name='Quantity', max_digits=18, decimal_places=6)),
                ('unit_price', satchmo_utils.fields.CurrencyField(verbose_name='Unit price', max_digits=18, decimal_places=10)),
                ('unit_tax', satchmo_utils.fields.CurrencyField(default=Decimal('0.00'), verbose_name='Unit tax', max_digits=18, decimal_places=10)),
                ('line_item_price', satchmo_utils.fields.CurrencyField(verbose_name='Line item price', max_digits=18, decimal_places=10)),
                ('tax', satchmo_utils.fields.CurrencyField(default=Decimal('0.00'), verbose_name='Line item tax', max_digits=18, decimal_places=10)),
                ('expire_date', models.DateField(help_text='Subscription expiration date.', null=True, verbose_name='Subscription End', blank=True)),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('discount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Line item discount', max_digits=18, decimal_places=10, blank=True)),
                ('order', models.ForeignKey(verbose_name='Order', to='shop.Order', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(on_delete=models.PROTECT, verbose_name='Product', to='product.Product')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Order Line Item',
                'verbose_name_plural': 'Order Line Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItemDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('price_change', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Price Change', max_digits=18, decimal_places=10, blank=True)),
                ('sort_order', models.IntegerField(help_text='The display order for this group.', verbose_name='Sort Order')),
                ('item', models.ForeignKey(verbose_name='Order Item', to='shop.OrderItem', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Order Item Detail',
                'verbose_name_plural': 'Order Item Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(blank=True, max_length=25, verbose_name='Payment Method')),
                ('amount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='amount', max_digits=18, decimal_places=10, blank=True)),
                ('time_stamp', models.DateTimeField(null=True, verbose_name='timestamp', blank=True)),
                ('transaction_id', models.CharField(max_length=45, null=True, verbose_name='Transaction ID', blank=True)),
                ('details', models.CharField(max_length=255, null=True, verbose_name='Details', blank=True)),
                ('reason_code', models.CharField(max_length=255, null=True, verbose_name='Reason Code', blank=True)),
                ('order', models.ForeignKey(related_name='payments', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Order Payment',
                'verbose_name_plural': 'Order Payments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderPaymentFailure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(blank=True, max_length=25, verbose_name='Payment Method')),
                ('amount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='amount', max_digits=18, decimal_places=10, blank=True)),
                ('time_stamp', models.DateTimeField(null=True, verbose_name='timestamp', blank=True)),
                ('transaction_id', models.CharField(max_length=45, null=True, verbose_name='Transaction ID', blank=True)),
                ('details', models.CharField(max_length=255, null=True, verbose_name='Details', blank=True)),
                ('reason_code', models.CharField(max_length=255, null=True, verbose_name='Reason Code', blank=True)),
                ('order', models.ForeignKey(related_name='paymentfailures', blank=True, to='shop.Order', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderPendingPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(blank=True, max_length=25, verbose_name='Payment Method')),
                ('amount', satchmo_utils.fields.CurrencyField(null=True, verbose_name='amount', max_digits=18, decimal_places=10, blank=True)),
                ('time_stamp', models.DateTimeField(null=True, verbose_name='timestamp', blank=True)),
                ('transaction_id', models.CharField(max_length=45, null=True, verbose_name='Transaction ID', blank=True)),
                ('details', models.CharField(max_length=255, null=True, verbose_name='Details', blank=True)),
                ('reason_code', models.CharField(max_length=255, null=True, verbose_name='Reason Code', blank=True)),
                ('capture', models.ForeignKey(related_name='pendingpayments', to='shop.OrderPayment', on_delete=models.CASCADE)),
                ('order', models.ForeignKey(related_name='pendingpayments', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Order Pending Payment',
                'verbose_name_plural': 'Order Pending Payments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(blank=True, max_length=20, verbose_name='Status', choices=[(b'Temp', 'Temp'), (b'New', 'New'), (b'Blocked', 'Blocked'), (b'In Process', 'In Process'), (b'Billed', 'Billed'), (b'Shipped', 'Shipped'), (b'Complete', 'Complete'), (b'Cancelled', 'Cancelled')])),
                ('notes', models.CharField(max_length=100, verbose_name='Notes', blank=True)),
                ('time_stamp', models.DateTimeField(verbose_name='Timestamp')),
                ('order', models.ForeignKey(verbose_name='Order', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('time_stamp',),
                'get_latest_by': 'time_stamp',
                'verbose_name': 'Order Status',
                'verbose_name_plural': 'Order Statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderTaxDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=50, verbose_name='Model')),
                ('description', models.CharField(max_length=50, verbose_name='Description', blank=True)),
                ('tax', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Tax', max_digits=18, decimal_places=10, blank=True)),
                ('order', models.ForeignKey(related_name='taxes', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Order tax detail',
                'verbose_name_plural': 'Order tax details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderVariable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(verbose_name='key')),
                ('value', models.CharField(max_length=100, verbose_name='value')),
                ('order', models.ForeignKey(related_name='variables', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'Order variable',
                'verbose_name_plural': 'Order variables',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderauthorization',
            name='capture',
            field=models.ForeignKey(related_name='authorizations', to='shop.OrderPayment', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderauthorization',
            name='order',
            field=models.ForeignKey(related_name='authorizations', to='shop.Order', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart',
            name='site',
            field=models.ForeignKey(verbose_name='Site', to='sites.Site', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]

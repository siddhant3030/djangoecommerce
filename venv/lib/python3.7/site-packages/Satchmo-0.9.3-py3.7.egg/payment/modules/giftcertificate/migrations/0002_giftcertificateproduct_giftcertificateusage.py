# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('giftcertificate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCertificateProduct',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='product.Product', verbose_name='Product', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Gift certificate product',
                'verbose_name_plural': 'Gift certificate products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GiftCertificateUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usage_date', models.DateField(null=True, verbose_name='Date of usage', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='Notes', blank=True)),
                ('balance_used', models.DecimalField(verbose_name='Amount Used', max_digits=8, decimal_places=2)),
                ('giftcertificate', models.ForeignKey(related_name='usages', to='giftcertificate.GiftCertificate', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

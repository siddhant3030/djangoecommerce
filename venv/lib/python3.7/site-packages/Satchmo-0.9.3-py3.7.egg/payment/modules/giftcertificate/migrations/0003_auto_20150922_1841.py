# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('sites', '0001_initial'),
        ('giftcertificate', '0002_giftcertificateproduct_giftcertificateusage'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcertificateusage',
            name='orderpayment',
            field=models.ForeignKey(verbose_name='Order Payment', to='shop.OrderPayment', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftcertificateusage',
            name='used_by',
            field=models.ForeignKey(related_name='giftcertificates_used', verbose_name='Used by', blank=True, to='contact.Contact', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftcertificate',
            name='order',
            field=models.ForeignKey(related_name='giftcertificates', verbose_name='Order', blank=True, to='shop.Order', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftcertificate',
            name='purchased_by',
            field=models.ForeignKey(related_name='giftcertificates_purchased', verbose_name='Purchased by', blank=True, to='contact.Contact', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftcertificate',
            name='site',
            field=models.ForeignKey(verbose_name='Site', blank=True, to='sites.Site', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
    ]

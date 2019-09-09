# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import satchmo_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingTier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=5, blank=True, help_text="This is the discount that will be applied to every product if no explicit Tiered Price exists for that product.  Leave as 0 if you don't want any automatic discount in that case.", null=True, verbose_name='Discount Percent')),
                ('group', models.OneToOneField(to='auth.Group', help_text='The user group that will receive the discount', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TieredPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', satchmo_utils.fields.CurrencyField(verbose_name='Price', max_digits=14, decimal_places=6)),
                ('quantity', models.DecimalField(default=b'1', help_text='Use this price only for this quantity or higher', verbose_name='Discount Quantity', max_digits=18, decimal_places=6)),
                ('expires', models.DateField(null=True, verbose_name='Expires', blank=True)),
                ('pricingtier', models.ForeignKey(related_name='tieredprices', to='tieredpricing.PricingTier', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(related_name='tieredprices', to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['pricingtier', 'expires', '-quantity'],
                'verbose_name': 'Tiered Price',
                'verbose_name_plural': 'Tiered Prices',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tieredprice',
            unique_together=set([('pricingtier', 'product', 'quantity', 'expires')]),
        ),
    ]

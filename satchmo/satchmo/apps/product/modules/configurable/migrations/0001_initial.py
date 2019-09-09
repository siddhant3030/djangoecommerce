# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurableProduct',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='product.Product', verbose_name='Product', on_delete=models.CASCADE)),
                ('create_subs', models.BooleanField(default=False, help_text="Create ProductVariations for all this product's options.  To use this, you must first add an option, save, then return to this page and select this option.", verbose_name='Create Variations')),
                ('option_group', models.ManyToManyField(to='product.OptionGroup', verbose_name='Option Group', blank=True)),
            ],
            options={
                'verbose_name': 'Configurable Product',
                'verbose_name_plural': 'Configurable Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='product.Product', verbose_name='Product', on_delete=models.CASCADE)),
                ('options', models.ManyToManyField(to='product.Option', verbose_name='Options')),
                ('parent', models.ForeignKey(verbose_name='Parent', to='configurable.ConfigurableProduct', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Product variation',
                'verbose_name_plural': 'Product variations',
            },
            bases=(models.Model,),
        ),
    ]

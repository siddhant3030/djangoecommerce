# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import satchmo_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomProduct',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='product.Product', verbose_name='Product', on_delete=models.CASCADE)),
                ('downpayment', models.IntegerField(default=20, verbose_name='Percent Downpayment')),
                ('deferred_shipping', models.BooleanField(default=False, help_text='Do not charge shipping at checkout for this item.', verbose_name='Deferred Shipping')),
                ('option_group', models.ManyToManyField(to='product.OptionGroup', verbose_name='Option Group', blank=True)),
            ],
            options={
                'verbose_name': 'Custom Product',
                'verbose_name_plural': 'Custom Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomTextField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Custom field name')),
                ('slug', models.SlugField(help_text='Auto-generated from name if blank', verbose_name='Slug', blank=True)),
                ('sort_order', models.IntegerField(default=0, help_text='The display order for this group.', verbose_name='Sort Order')),
                ('price_change', satchmo_utils.fields.CurrencyField(null=True, verbose_name='Price Change', max_digits=14, decimal_places=6, blank=True)),
                ('products', models.ForeignKey(related_name='custom_text_fields', verbose_name='Custom Fields', to='custom.CustomProduct', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('sort_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomTextFieldTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('name', models.CharField(max_length=255, verbose_name='Translated Custom Text Field Name')),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('customtextfield', models.ForeignKey(related_name='translations', to='custom.CustomTextField', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('customtextfield', 'name', 'languagecode'),
                'verbose_name': 'CustomTextField Translation',
                'verbose_name_plural': 'CustomTextField Translations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='customtextfieldtranslation',
            unique_together=set([('customtextfield', 'languagecode', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='customtextfield',
            unique_together=set([('slug', 'products')]),
        ),
    ]

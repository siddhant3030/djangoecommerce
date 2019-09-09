# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import keyedcache.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upsell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateField(verbose_name='Creation Date')),
                ('style', models.CharField(default=b'CHECKBOX_1_FALSE', max_length=20, verbose_name='Upsell Style', choices=[(b'CHECKBOX_1_FALSE', 'Checkbox to add 1'), (b'CHECKBOX_1_TRUE', 'Checkbox to add 1, checked by default'), (b'CHECKBOX_MATCH_FALSE', 'Checkbox to match quantity'), (b'CHECKBOX_MATCH_TRUE', 'Checkbox to match quantity, checked by default'), (b'FORM', 'Form with 0 quantity')])),
                ('notes', models.TextField(help_text='Internal notes', null=True, verbose_name='Notes', blank=True)),
                ('goal', models.ForeignKey(related_name='upsellgoals', verbose_name='Goal Product', to='product.Product', on_delete=models.CASCADE)),
                ('target', models.ManyToManyField(help_text='The products for which you want to show this goal product as an Upsell.', related_name='upselltargets', verbose_name='Target Product', to='product.Product')),
            ],
            options={
                'ordering': ('goal',),
            },
            bases=(models.Model, keyedcache.models.CachedObjectMixin),
        ),
        migrations.CreateModel(
            name='UpsellTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('languagecode', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'English')])),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('menu', models.ForeignKey(related_name='translations', to='upsell.Upsell', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('languagecode',),
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.DecimalField(help_text='% tax for this area and type', verbose_name='Percentage', max_digits=7, decimal_places=6)),
            ],
            options={
                'verbose_name': 'Tax Rate',
                'verbose_name_plural': 'Tax Rates',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCardDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit_type', models.CharField(max_length=16, verbose_name='Credit Card Type')),
                ('display_cc', models.CharField(max_length=4, verbose_name='CC Number (Last 4 digits)')),
                ('encrypted_cc', models.CharField(verbose_name='Encrypted Credit Card', max_length=40, null=True, editable=False, blank=True)),
                ('expire_month', models.IntegerField(verbose_name='Expiration Month')),
                ('expire_year', models.IntegerField(verbose_name='Expiration Year')),
                ('card_holder', models.CharField(max_length=60, verbose_name='card_holder Name', blank=True)),
                ('start_month', models.IntegerField(null=True, verbose_name='Start Month', blank=True)),
                ('start_year', models.IntegerField(null=True, verbose_name='Start Year', blank=True)),
                ('issue_num', models.CharField(max_length=2, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Credit Card',
                'verbose_name_plural': 'Credit Cards',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=20, verbose_name='Description')),
                ('active', models.BooleanField(default=False, help_text='Should this be displayed as an option for the user?', verbose_name='Active')),
                ('optionName', models.CharField(help_text='The class name as defined in payment.py', unique=True, max_length=20, verbose_name='Option Name')),
                ('sortOrder', models.IntegerField(verbose_name='Sort Order')),
            ],
            options={
                'verbose_name': 'Payment Option',
                'verbose_name_plural': 'Payment Options',
            },
            bases=(models.Model,),
        ),
    ]

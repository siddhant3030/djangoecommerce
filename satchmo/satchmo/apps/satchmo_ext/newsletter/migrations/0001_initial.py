# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscribed', models.BooleanField(default=True, verbose_name='Subscribed')),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('create_date', models.DateField(verbose_name='Creation Date')),
                ('update_date', models.DateField(verbose_name='Update Date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubscriptionAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(max_length=100, verbose_name='Attribute Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('subscription', models.ForeignKey(related_name='attributes', to='newsletter.Subscription', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Subscription Attribute',
                'verbose_name_plural': 'Subscription Attributes',
            },
            bases=(models.Model,),
        ),
    ]

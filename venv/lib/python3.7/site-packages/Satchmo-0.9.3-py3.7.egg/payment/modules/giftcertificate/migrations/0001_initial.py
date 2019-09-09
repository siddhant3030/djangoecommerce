# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCertificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100, null=True, verbose_name='Certificate Code', blank=True)),
                ('date_added', models.DateField(null=True, verbose_name='Date added', blank=True)),
                ('valid', models.BooleanField(default=True, verbose_name='Valid')),
                ('message', models.CharField(max_length=255, null=True, verbose_name='Message', blank=True)),
                ('recipient_email', models.EmailField(max_length=75, verbose_name='Email', blank=True)),
                ('start_balance', models.DecimalField(verbose_name='Starting Balance', max_digits=8, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Gift Certificate',
                'verbose_name_plural': 'Gift Certificates',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import product.modules.downloadable.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadableProduct',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='product.Product', verbose_name='Product', on_delete=models.CASCADE)),
                ('file', models.FileField(upload_to=product.modules.downloadable.models._protected_dir, verbose_name='File')),
                ('num_allowed_downloads', models.IntegerField(default=0, help_text='Number of times link can be accessed. Enter 0 for unlimited.', verbose_name='Num allowed downloads')),
                ('expire_minutes', models.IntegerField(default=0, help_text='Number of minutes the link should remain active. Enter 0 for unlimited.', verbose_name='Expire minutes')),
                ('active', models.BooleanField(default=True, help_text='Is this download currently active?', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Downloadable Product',
                'verbose_name_plural': 'Downloadable Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DownloadLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=40, verbose_name='Key')),
                ('num_attempts', models.IntegerField(verbose_name='Number of attempts')),
                ('time_stamp', models.DateTimeField(verbose_name='Time stamp')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('downloadable_product', models.ForeignKey(verbose_name='Downloadable product', to='downloadable.DownloadableProduct', on_delete=models.CASCADE)),
                ('order', models.ForeignKey(verbose_name='Order', to='shop.Order', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Download Link',
                'verbose_name_plural': 'Download Links',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcarddetail',
            name='orderpayment',
            field=models.ForeignKey(related_name='creditcards', to='shop.OrderPayment', unique=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_creditcarddetail_orderpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcarddetail',
            name='orderpayment',
            field=models.OneToOneField(related_name='creditcard', to='shop.OrderPayment', on_delete=models.CASCADE),
        ),
    ]

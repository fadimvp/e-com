# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20180730_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_total_price',
            field=models.DecimalField(default=2.99, max_digits=50, decimal_places=2),
        ),
    ]

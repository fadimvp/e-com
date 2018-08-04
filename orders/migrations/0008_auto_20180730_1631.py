# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20180730_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_total_price',
            field=models.DecimalField(max_digits=50, decimal_places=2),
        ),
    ]

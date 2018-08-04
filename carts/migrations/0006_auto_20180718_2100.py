# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20180718_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(default=26.0, max_digits=50, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(default=27.0, max_digits=50, decimal_places=2),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-09 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_purchase_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(editable=False, verbose_name=datetime.datetime(2022, 6, 9, 14, 42, 41, 290756)),
        ),
    ]

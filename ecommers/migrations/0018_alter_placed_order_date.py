# Generated by Django 4.0.4 on 2022-10-05 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0017_alter_placed_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placed_order',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-09-11 12:08

from django.db import migrations, models
import ecommers.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0003_products_products_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='products_Image',
            field=models.ImageField(upload_to=ecommers.models.path_and_rename),
        ),
    ]
# Generated by Django 4.0.4 on 2022-09-16 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0007_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_to_cart',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.products'),
        ),
        migrations.AlterField(
            model_name='add_to_cart',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.user'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-09-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0006_rename_username_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]

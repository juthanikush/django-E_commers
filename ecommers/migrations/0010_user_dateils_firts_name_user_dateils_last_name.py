# Generated by Django 4.0.4 on 2022-09-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0009_alter_user_dateils_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_dateils',
            name='firts_name',
            field=models.CharField(default=0, max_length=25),
        ),
        migrations.AddField(
            model_name='user_dateils',
            name='last_name',
            field=models.CharField(default=0, max_length=25),
        ),
    ]

# Generated by Django 3.2.5 on 2021-09-22 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_token_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_user',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.2.5 on 2021-09-21 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_column'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='column_name',
        ),
        migrations.RemoveField(
            model_name='column',
            name='order',
        ),
        migrations.RemoveField(
            model_name='column',
            name='show',
        ),
        migrations.AddField(
            model_name='column',
            name='data',
            field=models.JSONField(null=True, verbose_name='Data'),
        ),
    ]
# Generated by Django 3.2.5 on 2021-08-06 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('symbol', 'portfolio')},
        ),
    ]
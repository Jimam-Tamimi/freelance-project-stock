# Generated by Django 3.2.5 on 2021-09-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablestate',
            name='columnsorder',
        ),
        migrations.RemoveField(
            model_name='tablestate',
            name='columnsreorder',
        ),
        migrations.RemoveField(
            model_name='tablestate',
            name='columnsvisible',
        ),
        migrations.AddField(
            model_name='tablestate',
            name='columnsdata',
            field=models.CharField(max_length=5000, null=True, verbose_name='ColumnsData'),
        ),
    ]

# Generated by Django 3.2.5 on 2021-09-12 07:40

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_tablestate_statedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablestate',
            name='statedata',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-23 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModuleApp', '0002_phasebtc_phaseeth_phaseusdt_setphaseeth_setphaseusdt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phasebtc',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='phaseeth',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='phaseusdt',
            name='time_end',
        ),
        migrations.AlterField(
            model_name='user',
            name='referrer',
            field=models.IntegerField(null=True),
        ),
    ]

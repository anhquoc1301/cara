# Generated by Django 4.0.1 on 2023-06-20 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ModuleApp', '0010_alter_inputmoney_detail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tradeusdt',
            options={'ordering': ['create_at']},
        ),
    ]
# Generated by Django 3.1.2 on 2020-12-19 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_delivery_trxid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='trxId',
        ),
    ]

# Generated by Django 3.1.2 on 2020-12-20 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_delivery_trxid'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='trxId',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
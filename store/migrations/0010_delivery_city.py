# Generated by Django 3.1.2 on 2020-12-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_delivery_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
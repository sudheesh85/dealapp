# Generated by Django 3.1.2 on 2020-12-06 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20201206_0424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_vendor',
            name='numberOfRedeemableCoins',
        ),
    ]

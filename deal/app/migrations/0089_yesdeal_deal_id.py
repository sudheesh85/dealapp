# Generated by Django 3.1.2 on 2021-05-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0088_remove_yesdeal_deal_qrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='yesdeal',
            name='deal_id',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]

# Generated by Django 3.1.2 on 2021-05-05 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0083_deal_scratch'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='user_lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='user_long',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
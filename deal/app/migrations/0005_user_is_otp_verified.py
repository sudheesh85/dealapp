# Generated by Django 3.0.5 on 2020-09-13 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200912_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_otp_verified',
            field=models.NullBooleanField(default=False),
        ),
    ]
# Generated by Django 3.0.5 on 2020-09-21 01:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200921_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='vendor_is_followed',
        ),
    ]
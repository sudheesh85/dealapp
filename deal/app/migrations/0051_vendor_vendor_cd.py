# Generated by Django 3.1.2 on 2020-12-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20201222_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_cd',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
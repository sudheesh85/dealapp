# Generated by Django 3.1.2 on 2021-02-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20210214_0321'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vendor_login',
        ),
        migrations.AddField(
            model_name='vendor',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='user_name',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendor_token',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_whatsapp',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
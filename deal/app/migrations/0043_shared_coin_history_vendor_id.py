# Generated by Django 3.1.2 on 2020-12-06 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_remove_user_vendor_numberofredeemablecoins'),
    ]

    operations = [
        migrations.AddField(
            model_name='shared_coin_history',
            name='vendor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vendor'),
        ),
    ]

# Generated by Django 3.1.2 on 2021-02-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_auto_20210221_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='item_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_img1',
            field=models.ImageField(blank=True, null=True, upload_to='yesdeal/media/vendor'),
        ),
        migrations.AlterField(
            model_name='yesdeal',
            name='deal_img1',
            field=models.ImageField(blank=True, null=True, upload_to='yesdeal/media/deal'),
        ),
    ]
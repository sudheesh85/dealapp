# Generated by Django 3.1.2 on 2021-03-01 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0071_auto_20210301_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='yesdeal',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]

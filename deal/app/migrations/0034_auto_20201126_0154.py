# Generated by Django 3.1.2 on 2020-11-26 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_user_service_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='service_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.area'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-26 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20201126_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='service_area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.area'),
        ),
    ]

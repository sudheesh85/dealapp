# Generated by Django 3.1.2 on 2020-10-24 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20201024_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='yesdeal',
            name='deal_available_branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.branch'),
        ),
    ]

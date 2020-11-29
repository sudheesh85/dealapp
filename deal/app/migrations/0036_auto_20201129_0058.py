# Generated by Django 3.1.2 on 2020-11-29 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20201126_0312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AddField(
            model_name='yesdeal',
            name='deal_category_on_age',
            field=models.TextField(blank=True, choices=[('18-30', '18-30'), ('31-40', '31-40'), ('41-50', '41-50'), ('51-60', '51-60'), ('61-Above', '61-Above')], default=''),
        ),
        migrations.AddField(
            model_name='yesdeal',
            name='deal_category_on_gender',
            field=models.TextField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default=''),
        ),
    ]

# Generated by Django 3.0.5 on 2020-09-28 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200926_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EXP_TIME', models.IntegerField(default=0)),
            ],
        ),
    ]

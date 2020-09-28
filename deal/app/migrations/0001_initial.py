# Generated by Django 3.0.5 on 2020-09-26 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceLoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(blank=True, max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=10, unique=True)),
                ('description', models.TextField(blank=True)),
                ('totalDeals', models.CharField(blank=True, max_length=5)),
                ('totalActiveDeals', models.CharField(blank=True, max_length=5)),
                ('numberOfRedeemableCoins', models.CharField(blank=True, max_length=5)),
                ('totalCollectedDeals', models.CharField(blank=True, max_length=5)),
            ],
        ),
    ]

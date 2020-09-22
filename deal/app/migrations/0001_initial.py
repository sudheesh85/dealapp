# Generated by Django 3.0.5 on 2020-09-09 21:00

from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


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
                ('loc_id', models.IntegerField()),
                ('location', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userCD', models.CharField(blank=True, max_length=6, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('nick_name', models.CharField(max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('gender', models.TextField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='')),
                ('dob', models.DateField(null=True)),
                ('mobile', models.BigIntegerField(blank=True, unique=True)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_gen_time', models.DateTimeField(null=True)),
                ('device_token', models.CharField(blank=True, default='', max_length=100)),
                ('interest', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[['Food', 'Food'], ['Outdoor', 'Outdoor'], ['Electronics', 'Electronics']], default='', max_length=24)),
                ('status', models.TextField(blank=True, choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('SUSPENDED', 'SUSPENDED')], default='')),
                ('no_of_coins', models.FloatField(blank=True, default=0.0)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('serviceLoc', models.TextField(blank=True, choices=[['Kochi', 'Kochi']], default='')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
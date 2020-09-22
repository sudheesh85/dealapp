# Generated by Django 3.0.5 on 2020-09-21 01:30

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_vendor_vendor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interested_vendors',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[['Lulu Hypermarket', 'Lulu Hypermarket']], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='vendor_is_followed',
            field=models.NullBooleanField(default=False),
        ),
    ]
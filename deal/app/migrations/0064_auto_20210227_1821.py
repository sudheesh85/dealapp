# Generated by Django 3.1.2 on 2021-02-27 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_vendor_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal_img_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_title', models.CharField(max_length=50, null=True)),
                ('deal_img', models.ImageField(blank=True, null=True, upload_to='yesdeal/media/deal')),
                ('img_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.interest')),
            ],
        ),
        migrations.CreateModel(
            name='Deal_img_vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_title', models.CharField(max_length=50, null=True)),
                ('deal_img', models.ImageField(blank=True, null=True, upload_to='yesdeal/media/vendor')),
                ('vendor_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.AlterField(
            model_name='yesdeal',
            name='deal_status',
            field=models.TextField(blank=True, choices=[('ACTIVE', 'ACTIVE'), ('CONFIRMED', 'CONFIRMED'), ('ON HOLD', 'ON HOLD'), ('DEACTIVATE', 'DEACTIVATE')], default=''),
        ),
        migrations.DeleteModel(
            name='Deal_img',
        ),
    ]

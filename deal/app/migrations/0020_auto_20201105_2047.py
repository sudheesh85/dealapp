# Generated by Django 3.1.2 on 2020-11-05 20:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20201102_0319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='numberOfRedeemableCoins',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='totalCollectedDeals',
        ),
        migrations.CreateModel(
            name='User_Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_is_followed', models.BooleanField(default=False, null=True)),
                ('numberOfRedeemableCoins', models.CharField(blank=True, max_length=5)),
                ('totalCollectedDeals', models.CharField(blank=True, max_length=5)),
                ('userCD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('vendor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='User_Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_collected', models.BooleanField(default=False, null=True)),
                ('collected_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('QR_code', models.ImageField(blank=True, null=True, upload_to='qrcode')),
                ('is_deal_redeemed', models.BooleanField(default=False, null=True)),
                ('deal_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.yesdeal')),
                ('userCD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('vendor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
    ]

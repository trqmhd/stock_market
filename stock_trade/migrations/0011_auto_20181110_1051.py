# Generated by Django 2.1.1 on 2018-11-10 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0002_auto_20181105_0328'),
        ('stock_trade', '0010_auto_20181110_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='stock_info',
        ),
        migrations.AddField(
            model_name='trade',
            name='stock_info',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='stock_info.StockInfo'),
        ),
    ]
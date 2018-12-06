# Generated by Django 2.1.1 on 2018-11-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0002_auto_20181105_0328'),
        ('stock_trade', '0004_trade_stock_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='stock_info',
        ),
        migrations.AddField(
            model_name='trade',
            name='stock_info',
            field=models.ManyToManyField(to='stock_info.StockInfo'),
        ),
    ]

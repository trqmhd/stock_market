# Generated by Django 2.1.1 on 2018-11-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0002_auto_20181105_0328'),
        ('stock_trade', '0011_auto_20181110_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='stock_info',
        ),
        migrations.AddField(
            model_name='trade',
            name='stock_name',
            field=models.ManyToManyField(to='stock_info.StockInfo'),
        ),
    ]

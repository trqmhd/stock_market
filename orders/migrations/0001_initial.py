# Generated by Django 2.1.1 on 2018-11-20 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock_trade', '0015_auto_20181112_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid')], default='created', max_length=200)),
                ('estimated_cost', models.DecimalField(decimal_places=5, default=0.0, max_digits=10)),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_trade.Trade')),
            ],
        ),
    ]

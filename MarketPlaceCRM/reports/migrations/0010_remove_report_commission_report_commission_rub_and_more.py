# Generated by Django 5.0.4 on 2024-06-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_remove_report_total_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='commission',
        ),
        migrations.AddField(
            model_name='report',
            name='commission_rub',
            field=models.IntegerField(default=0, verbose_name='commission_rub'),
        ),
        migrations.AddField(
            model_name='report',
            name='commission_uan',
            field=models.IntegerField(default=0, verbose_name='commission_uan'),
        ),
    ]

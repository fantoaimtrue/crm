# Generated by Django 5.0.4 on 2024-06-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0012_alter_report_commission_rub_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='last_insurance',
            field=models.FloatField(default=0, verbose_name='last_insurance'),
        ),
    ]

# Generated by Django 5.0.4 on 2024-06-25 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_report_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='product_id',
        ),
    ]

# Generated by Django 5.0.4 on 2024-09-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0007_rename_telegram_id_profile_tg_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tg_username',
            field=models.TextField(null=True),
        ),
    ]
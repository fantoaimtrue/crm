# Generated by Django 5.0.4 on 2024-09-25 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0006_alter_profile_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='telegram_id',
            new_name='tg_username',
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-09 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0004_alter_telegramuser_chat_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuser',
            old_name='chat_id',
            new_name='user_id',
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0005_rename_chat_id_telegramuser_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='rate_limit',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-09 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0002_telegramuser_rename_text_question_text_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='chat_id',
            field=models.CharField(max_length=50),
        ),
    ]

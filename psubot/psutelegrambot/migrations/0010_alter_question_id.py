# Generated by Django 4.1.7 on 2023-03-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0009_alter_question_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

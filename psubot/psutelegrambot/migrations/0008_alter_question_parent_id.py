# Generated by Django 4.1.7 on 2023-03-15 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0007_remove_telegramuser_rate_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='psutelegrambot.question'),
        ),
    ]

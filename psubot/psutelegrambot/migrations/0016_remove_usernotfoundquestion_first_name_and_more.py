# Generated by Django 4.1.7 on 2023-04-10 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0015_remove_usernotfoundquestion_isissueresolved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='user_language_code',
        ),
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='username',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usernotfoundquestion',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='psutelegrambot.telegramuser'),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-04 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0014_alter_usernotfoundquestion_question_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotfoundquestion',
            name='isIssueResolved',
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-19 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psutelegrambot', '0008_alter_question_parent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
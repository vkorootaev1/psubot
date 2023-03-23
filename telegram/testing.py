import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'psubot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"
django.setup()

from psutelegrambot.models import Question, TelegramUser

q = Question(id=20, parent_id=None, text_ru='ru20', text_en='en20')
q.save()




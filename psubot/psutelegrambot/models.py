from django.db import models
from django.utils import timezone


class Question(models.Model):
    parent_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    text_ru = models.TextField()
    text_en = models.TextField()

    def __str__(self):
        return f"{self.pk}; {self.text_ru}; {self.text_en}"


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    language_code = models.SmallIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_id}; {self.language_code}"


class UserNotFoundQuestion(models.Model):
    user = models.ForeignKey(TelegramUser, to_field='user_id', on_delete=models.CASCADE)
    message_id = models.BigIntegerField()
    text = models.TextField()
    question_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}; {self.message_id}; {self.text}"

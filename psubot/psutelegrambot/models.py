from django.db import models


class Question(models.Model):
    parent_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    text_ru = models.TextField()
    text_en = models.TextField()

    def __str__(self):
        return f"{self.pk}; {self.text_ru}; {self.text_en}"


class TelegramUser(models.Model):
    user_id = models.BigIntegerField()
    language_code = models.SmallIntegerField()

    def __str__(self):
        return f"{self.user_id}; {self.language_code}"

from django.contrib import admin
from psutelegrambot.models import UserNotFoundQuestion


class UserNotFoundQuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserNotFoundQuestion, UserNotFoundQuestionAdmin)

# Register your models here.

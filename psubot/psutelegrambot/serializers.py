from rest_framework import serializers
from .models import Question, UserNotFoundQuestion, TelegramUser
from rest_framework_recursive.fields import RecursiveField


# Рекурсивный сериализатор для дерева
class TreeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Question
        fields = ('id', 'parent_id', 'text_ru', 'text_en', 'children')


# Сериализатор для отдельных вершин
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'parent_id', 'text_ru', 'text_en')


# Сериализатор для корневых вопросов
class ListOfRootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'parent_id', 'text_ru', 'text_en')


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'


class UserNotFoundQuestionSerializer(serializers.ModelSerializer):
    question_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    user = TelegramUserSerializer(read_only=True)

    class Meta:
        model = UserNotFoundQuestion
        fields = '__all__'
